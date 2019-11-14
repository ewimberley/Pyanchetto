import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
promotion_candidates = ("Q", "R", "B", "N")
rook_positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
king_positions = [(4, 0), (4, 7)]
king_castle_end_positions = [(2, 0, False), (6, 0, False), (2, 7, False), (6, 7, False)]
rook_castle_end_positions = [(3, 0, False), (5, 0, False), (3, 7, False), (5, 7, False)]
all_coords = [(i, j) for i in range(SIZE) for j in range(SIZE)]
knight_warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
king_warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
pawn_capture_warps = [[(-1, 1), (1, 1)], [(-1, -1), (1, -1)]]
EMPTY = 0
WHITE = 1
BLACK = 2

def inc(x): return x + 1
def dec(x): return x - 1
def same(x): return x
def file_to_index(file): return ord(file) - 97
def in_range(coord): return coord[0] in range(SIZE) and coord[1] in range(SIZE)
def inverse_color(color): return WHITE if color == BLACK else BLACK
def map2(func, vals): return [func(val) for val in vals] #map with side effects
def threatened_str(threatened):
    piece_arr = [str(threatened[coord[1]][SIZE - coord[0] - 1]) for coord in all_coords]
    return "".join([" ".join(piece_arr[i*SIZE:i*SIZE+SIZE])+"\n" for i in range(SIZE)])

class BadMoveException(Exception):
    pass

class BadPromotionException(Exception):
    pass

class Chess:

    def __init__(self):
        self.current_player = 1
        self.move_list = []
        self.threatened = None
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.rooks_moved = np.zeros(4, dtype=np.bool_)
        self.kings_moved = np.zeros(2, dtype=np.bool_)
        self.__set_row(0, home_row)
        self.__set_row(1, ["P"] * 8)
        self.__set_row(6, ["p"] * 8)
        self.__set_row(7, [p.lower() for p in home_row])

    def coord(self, coord, piece=None):
        if piece is None:
            return self.board[coord[1]][coord[0]]
        self.board[coord[1]][coord[0]] = piece

    def is_color(self, coord, color): return self.color(coord) == color

    def color(self, coord):
        if self.board[coord[1]][coord[0]] == EMPTY:
            return EMPTY
        return WHITE if self.board[coord[1]][coord[0]] < pieces.index("k") else BLACK

    def is_type(self, coord, piece_type): return pieces[self.coord(coord)].lower() == piece_type.lower()

    def player_pieces_of_type(self, piece_type, player):
        return [coord for coord in self.pieces_of_type(piece_type) if self.is_color(coord, player)]

    def player_pieces(self, player): return [coord for coord in all_coords if self.is_color(coord, player)]

    def pieces_of_type(self, piece_type):
        indices = (pieces.index(piece_type), pieces.index(piece_type.lower()))
        return [coord for coord in all_coords if self.coord(coord) in indices]

    def valid_moves(self):
        self.threatened = None #King's current threats are not thwarted by threats
        self.threatened = self._compute_threatened(self.current_player)
        moves = self.valid_moves_for_player(self.current_player)
        self.threatened = None
        return moves

    def valid_moves_for_player(self, player):
        return [(piece, move) for piece in self.player_pieces(player) for move in self.valid_piece_moves(piece)]

    def valid_piece_moves(self, piece):
        # TODO current player cannot make a move that puts their king in check
        # TODO capturing the king is not a valid move
        # TODO detect check and checkmate
        piece_type = self.coord(piece)
        move_funcs = [lambda: [], self.king, self.queen, self.rook, self.bishop, self.knight, self.pawn]
        piece_type = piece_type - 6 if piece_type > 6 else piece_type
        moves = move_funcs[piece_type](piece[0], piece[1])
        return moves

    def _compute_threatened(self, player):
        opponent_moves = self.valid_moves_for_player(inverse_color(player))
        opponent_pawns = self.player_pieces_of_type("P", inverse_color(player))
        opponent_moves.extend([(pawn, move) for pawn in opponent_pawns for move in self.pawn_threats(pawn[0], pawn[1])])
        threatened = np.zeros((8, 8), dtype=np.int8)
        for move in opponent_moves:
            threatened[move[1][0]][move[1][1]] += 1 if move[1][2] else 0
        return threatened

    def check_check(self, moves):
        kings = self.pieces_of_type("K")
        return True in [((move[1][0], move[1][1]) == king and move[1][2]) for king in kings for move in moves]

    def move(self, from_coord, to_coord):
        valid = self.valid_moves()
        if (from_coord, to_coord) in valid:
            if self.is_type(from_coord, "R") and from_coord in rook_positions:
                self.rooks_moved[rook_positions.index(from_coord)] = True
            elif self.is_type(from_coord, "K") and from_coord in king_positions:
                self.kings_moved[king_positions.index(from_coord)] = True
                if to_coord in king_castle_end_positions:
                    rook_index = king_castle_end_positions.index(to_coord)
                    self.__move(rook_positions[rook_index], rook_castle_end_positions[rook_index])
            #TODO add captured pieces to capture list
            self.__move(from_coord, to_coord)
            self.move_list.append((from_coord, to_coord))
            if len(to_coord) == 4:
                self.__handle_promotion(to_coord)
            self.current_player = inverse_color(self.current_player)
        else:
            raise BadMoveException("Move is invalid")

    def __move(self, from_coord, to_coord):
        self.coord(to_coord, self.coord(from_coord))
        self.coord(from_coord, EMPTY)

    def __handle_promotion(self, to_coord):
        promotion_type = to_coord[3]
        if promotion_type.upper() in promotion_candidates and self.is_type(to_coord, "P"):
            if self.current_player == WHITE and to_coord[1] == 7:
                self.coord(to_coord, pieces.index(promotion_type.upper()))
            elif self.current_player == BLACK and to_coord[1] == 0:
                self.coord(to_coord, pieces.index(promotion_type.lower()))
            else:
                raise BadPromotionException("Cannot promote from this position")
        else:
            raise BadPromotionException("Invalid promotion")

    def pawn_threats(self, f, r):
        color = self.color((f, r))
        return self.__warps([], (f, r), pawn_capture_warps[color - 1], (color,))

    def pawn(self, f, r):
        # TODO en pessant
        color = self.color((f, r))
        warps = [[(0, 1), (0, 2)] if r == 1 and self.is_color((f, r + 1), EMPTY) else [(0, 1)]]
        warps.append([(0, -1), (0, -2)] if r == 6 and self.is_color((f, r - 1), EMPTY) else [(0, -1)])
        moves = self.__warps([], (f, r), warps[color - 1], (WHITE, BLACK), False)
        moves = self.__warps(moves, (f, r), pawn_capture_warps[color - 1], (EMPTY, color))
        final_moves = []
        for move in moves:
            if color == WHITE and move[1] == 7:
                final_moves.extend([(move[0], move[1], move[2], promotion) for promotion in promotion_candidates])
            elif color == BLACK and move[1] == 0:
                final_moves.extend([(move[0], move[1], move[2], promotion.lower()) for promotion in promotion_candidates])
            else:
                final_moves.append(move)
        return final_moves

    def rook(self, f, r): return self.orthogonal([], f, r)

    def bishop(self, f, r): return self.diagonal([], f, r)

    def knight(self, f, r): return self.__warps([], (f, r), knight_warps, (self.color((f, r)),))

    def queen(self, f, r): return self.orthogonal(self.diagonal([], f, r), f, r)

    def king(self, f, r):
        color = self.color((f, r))
        castle_moves = []
        if not self.kings_moved[color - 1]:
            if not self.rooks_moved[0 if color == WHITE else 2] and self.positions_clear([(1, r), (2, r), (3, r)]):
                castle_moves.append((2, r, False))
            if not self.rooks_moved[1 if color == WHITE else 3] and self.positions_clear([(5, r), (6, r)]):
                castle_moves.append((6, r, False))
        return self.__warps(castle_moves, (f, r), king_warps, (color,))

    def positions_clear(self, coords):
        for coord in coords:
            status = 0 if self.threatened is None else self.threatened[coord[0]][coord[1]]
            if self.coord(coord) != 0 or status != 0:
                return False
        return True

    def __warps(self, moves, coord, warps, excluded, threat=True):
        warps = [(coord[0] + w[0], coord[1] + w[1], threat) for w in warps]
        moves.extend([w for w in warps if in_range(w) and self.color(w) not in excluded])
        return moves

    def orthogonal(self, moves, f, r): return self.__vectors(moves, f, r, [(inc, same), (dec, same), (same, inc), (same, dec)])

    def diagonal(self, moves, f, r): return self.__vectors(moves, f, r, [(inc, inc), (dec, dec), (inc, dec), (dec, inc)])

    def __vectors(self, moves, f, r, funcs_list):
        map2(lambda funcs: self.__vector(moves, f, r, funcs), [funcs for funcs in funcs_list])
        return moves

    def __vector(self, moves, f, r, funcs):
        color = self.color((f, r))
        coord = (funcs[1](f), funcs[0](r), True)
        while in_range(coord) and self.color(coord) in (inverse_color(color), EMPTY):
            moves.append(coord)
            if self.color(coord) == inverse_color(color):
                break
            coord = (funcs[1](coord[0]), funcs[0](coord[1]), coord[2])
        return moves

    def __set_row(self, row, row_pieces):
        map2(lambda col: self.coord((col, row), pieces.index(row_pieces[col])), [col for col in range(SIZE)])

    def __str__(self):
        piece_arr = [pieces_ascii[self.coord((coord[1], SIZE - coord[0] - 1))] for coord in all_coords]
        return "".join([" ".join(piece_arr[i*SIZE:i*SIZE+SIZE])+"\n" for i in range(SIZE)])

    def hash(self):
        #TODO add rook and king moved state?
        return "".join([pieces[self.coord((coord[1], SIZE - coord[0] - 1))] for coord in all_coords])

    def clone(self):
        #TODO use deepcopy instead?
        clone = Chess()
        clone.current_player = self.current_player
        clone.move_list = self.move_list.copy()
        clone.board = np.copy(self.board)
        clone.rooks_moved = np.copy(self.rooks_moved)
        clone.kings_moved = np.copy(self.kings_moved)
        return clone
