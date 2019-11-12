import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
promotion_candidates = ("Q", "R", "B", "N")
rook_positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
king_positions = [(4, 0), (4, 7)]
king_castle_end_positions = [(2, 0), (6, 0), (2, 7), (6, 7)]
rook_castle_end_positions = [(3, 0), (5, 0), (3, 7), (5, 7)]
all_coords = [(i, j) for i in range(SIZE) for j in range(SIZE)]
knight_warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
king_warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
EMPTY = 0
WHITE = 1
BLACK = 2

def inc(x): return x + 1
def dec(x): return x - 1
def ident(x): return x
def file_to_index(file): return ord(file) - 97
def coord_in_range(coord): return coord[0] in range(SIZE) and coord[1] in range(SIZE)

class BadMoveException(Exception):
    pass

class BadPromotionException(Exception):
    pass

class Chess:

    def __init__(self):
        self.current_player = 1
        self.move_list = []
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.threatened = np.zeros((8, 8), dtype=np.int8)
        self.rooks_moved = np.zeros(4, dtype=np.bool_)
        self.kings_moved = np.zeros(2, dtype=np.bool_)
        self.__set_row(0, home_row)
        self.__set_row(1, ["P"] * 8)
        self.__set_row(6, ["p"] * 8)
        self.__set_row(7, [p.lower() for p in home_row])

    def get_coord(self, coord): return self.board[coord[1]][coord[0]]

    def set_coord(self, coord, piece): self.board[coord[1]][coord[0]] = piece

    def is_color(self, coord, color): return self.color(coord) == color

    def move(self, from_coord, to_coord):
        promotion_type = None if len(to_coord) == 2 else to_coord[2]
        if (from_coord, to_coord) in self.valid_moves():
            if self.coord_is_type(from_coord, "R") and from_coord in rook_positions:
                self.rooks_moved[rook_positions.index(from_coord)] = True
            elif self.coord_is_type(from_coord, "K") and from_coord in king_positions:
                self.kings_moved[king_positions.index(from_coord)] = True
                if to_coord in king_castle_end_positions:
                    rook_index = king_castle_end_positions.index(to_coord)
                    self.__move(rook_positions[rook_index], rook_castle_end_positions[rook_index])
            self.__move(from_coord, to_coord)
            self.move_list.append((from_coord, to_coord))
            if promotion_type is not None:
                self.__handle_promotion(promotion_type, to_coord)
            self.current_player = WHITE if self.current_player == BLACK else BLACK
        else:
            raise BadMoveException("Move is invalid")

    def __move(self, from_coord, to_coord):
        self.set_coord(to_coord, self.get_coord(from_coord))
        self.set_coord(from_coord, EMPTY)

    def __handle_promotion(self, promotion_type, to_coord):
        if promotion_type.upper() in promotion_candidates and self.coord_is_type(to_coord, "P"):
            if self.current_player == WHITE and to_coord[1] == 7:
                self.set_coord(to_coord, pieces.index(promotion_type.upper()))
            elif self.current_player == BLACK and to_coord[1] == 0:
                self.set_coord(to_coord, pieces.index(promotion_type.lower()))
            else:
                raise BadPromotionException("Cannot promote from this position")
        else:
            raise BadPromotionException("Invalid promotion")

    def coord_is_type(self, coord, piece_type):
        return pieces[self.get_coord(coord)].lower() == piece_type.lower()

    def valid_moves(self):
        return [(piece, move) for piece in self.player_pieces() for move in self.valid_piece_moves(piece)]

    def player_pieces_of_type(self, piece_type):
        return [coord for coord in self.pieces_of_type(piece_type) if self.is_color(coord, self.current_player)]

    def player_pieces(self):
        return [coord for coord in all_coords if self.is_color(coord, self.current_player)]

    def pieces_of_type(self, piece_type):
        indices = (pieces.index(piece_type), pieces.index(piece_type.lower()))
        return [coord for coord in all_coords if self.get_coord(coord) in indices]

    def valid_piece_moves(self, piece):
        # TODO current player cannot make a move that puts their king in check
        # TODO capturing the king is not a valid move
        # TODO detect check and checkmate
        piece_type = self.get_coord(piece)
        move_funcs = [lambda: [], self.king, self.queen, self.rook, self.bishop, self.knight, self.pawn]
        piece_type = piece_type - 6 if piece_type > 6 else piece_type
        moves = move_funcs[piece_type](piece[0], piece[1])
        return moves

    def check_check(self, moves):
        for king in self.pieces_of_type("K"):
            for move in moves:
                if move[1] == king:
                    return True
        return False

    def pawn(self, file, rank):
        # TODO en pessant
        color = self.color((file, rank))
        first_move = (color == WHITE and rank == 1) or (color == BLACK and rank == 6)
        if color == WHITE:
            warps = [(0, 1), (0, 2)] if first_move and self.is_color((file, rank + 1), EMPTY) else [(0, 1)]
            capture_warps = [(-1, 1), (1, 1)]
        elif color == BLACK:
            warps = [(0, -1), (0, -2)] if first_move and self.is_color((file, rank - 1), EMPTY) else [(0, -1)]
            capture_warps = [(-1, -1), (1, -1)]
        moves = self.apply_warps([], (file, rank), warps, (WHITE, BLACK))
        moves = self.apply_warps(moves, (file, rank), capture_warps, (EMPTY, color))
        final_moves = []
        for move in moves:
            if color == WHITE and move[1] == 7:
                final_moves.extend([(move[0], move[1], promotion) for promotion in promotion_candidates])
            elif color == BLACK and move[1] == 0:
                final_moves.extend([(move[0], move[1], promotion.lower()) for promotion in promotion_candidates])
            else:
                final_moves.append(move)
        return final_moves

    def rook(self, file, rank):
        moves = self.valid_vertical_moves([], file, rank)
        return self.valid_horizontal_moves(moves, file, rank)

    def bishop(self, file, rank): return self.valid_diagonal_moves([], file, rank)

    def knight(self, file, rank): return self.apply_warps([], (file, rank), knight_warps, (self.color((file, rank)),))

    def queen(self, file, rank):
        moves = self.valid_diagonal_moves([], file, rank)
        self.valid_vertical_moves(moves, file, rank)
        return self.valid_horizontal_moves(moves, file, rank)

    def king(self, file, rank):
        color = self.color((file, rank))
        castle_moves = []
        if not self.kings_moved[color-1]:
            #TODO check if king has to move through check
            if not self.rooks_moved[0 if color == WHITE else 2] and self.positions_clear([(1, rank), (2, rank), (3, rank)]):
                castle_moves.append((2, rank))
            if not self.rooks_moved[1 if color == WHITE else 3] and self.positions_clear([(5, rank), (6, rank)]):
                castle_moves.append((6, rank))
        return self.apply_warps(castle_moves, (file, rank), king_warps, (color,))

    def positions_clear(self, coords):
        for coord in coords:
            if self.get_coord(coord) != 0:
                return False
        return True

    def apply_warps(self, moves, original, warps, excluded_colors):
        for warp in warps:
            new_coord = (original[0] + warp[0], original[1] + warp[1])
            if coord_in_range(new_coord) and self.color(new_coord) not in excluded_colors:
                moves.append(new_coord)
        return moves

    def valid_vertical_moves(self, moves, file, rank):
        return self.__valid_moves_vectors(moves, rank, file, [(inc, ident), (dec, ident)])

    def valid_horizontal_moves(self, moves, file, rank):
        return self.__valid_moves_vectors(moves, rank, file, [(ident, inc), (ident, dec)])

    def valid_diagonal_moves(self, moves, file, rank):
        return self.__valid_moves_vectors(moves, rank, file, [(inc, inc), (dec, dec), (inc, dec), (dec, inc)])

    def __valid_moves_vectors(self, moves, rank, file, func_list):
        for func in func_list:
            self.__valid_moves_vector(moves, rank, file, func)
        return moves

    def __valid_moves_vector(self, moves, rank, file, func):
        color = self.color((file, rank))
        on_coord = (func[1](file), func[0](rank))
        while coord_in_range(on_coord):
            move_color = self.color(on_coord)
            if move_color != EMPTY:
                if move_color != color:
                    moves.append(on_coord)
                break
            moves.append(on_coord)
            on_coord = (func[1](on_coord[0]), func[0](on_coord[1]))
        return moves

    def color(self, coord):
        if self.board[coord[1]][coord[0]] == EMPTY:
            return EMPTY
        return WHITE if self.board[coord[1]][coord[0]] < pieces.index("k") else BLACK

    def __set_row(self, row, row_pieces):
        for col in range(SIZE):
            self.board[row][col] = pieces.index(row_pieces[col])

    def __str__(self):
        board_str = ""
        for coord in all_coords:
            board_str += pieces_ascii[self.get_coord((coord[1], SIZE-coord[0]-1))] + " "
            board_str += "\n" if coord[1] == 7 else ""
        return board_str

    def hash(self):
        #TODO add rook and king moved state?
        return "".join([pieces[self.get_coord((coord[1], SIZE-coord[0]-1))] for coord in all_coords])

    def clone(self):
        #TODO use deepcopy instead?
        clone = Chess()
        clone.current_player = self.current_player
        clone.move_list = self.move_list.copy()
        clone.board = np.copy(self.board)
        clone.rooks_moved = np.copy(self.rooks_moved)
        clone.kings_moved = np.copy(self.kings_moved)
        return clone
