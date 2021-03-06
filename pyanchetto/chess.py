import numpy as np
import copy
import math

SIZE = 8
piece_types = ("K", "Q", "R", "B", "N", "P")
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_index = {pieces[i]: i for i in range(len(pieces))}
pieces_type_map = {p_type: (pieces_index[p_type], pieces_index[p_type.lower()]) for p_type in piece_types}
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
promotion_candidates = ("Q", "R", "B", "N")
rook_positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
rook_positions_index = {rook_positions[i]: i for i in range(len(rook_positions))}
king_positions = [(4, 0), (4, 7)]
king_castle_end_positions = [(2, 0, False), (6, 0, False), (2, 7, False), (6, 7, False)]
king_castle_end_positions_index = {king_castle_end_positions[i]: i for i in range(len(king_castle_end_positions))}
rook_castle_end_positions = [(3, 0, False), (5, 0, False), (3, 7, False), (5, 7, False)]
rook_castle_end_positions_index = {rook_castle_end_positions[i]: i for i in range(len(rook_castle_end_positions))}
all_coords = [(i, j) for i in range(SIZE) for j in range(SIZE)]
knight_warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
king_warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
pawn_capture_warps = [[(-1, 1), (1, 1)], [(-1, -1), (1, -1)]]
EMPTY, WHITE, BLACK = 0, 1, 2
NORMAL, CHECK, CHECKMATE, STALEMATE = 0, 1, 2, 3

def file_to_index(file): return ord(file) - 97
def index_to_file(index): return chr(index + 97)
def rank_file_to_coord(to_rank_file): return (file_to_index(to_rank_file[0]), int(to_rank_file[1]) - 1)
def coord_to_notation(coord): return index_to_file(coord[0]) + str(coord[1]+1)
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

    def __init__(self, other=None):
        if other is not None:
            self.board = np.copy(other.board)
            self.rooks_moved = copy.deepcopy(other.rooks_moved)
            self.kings_moved = copy.deepcopy(other.kings_moved)
            self.current_player = other.current_player
            self.move_list = copy.deepcopy(other.move_list)
            self.pgn_str = copy.deepcopy(other.pgn_str)
            self.captured_pieces = copy.deepcopy(other.captured_pieces)
            self.promoted_pieces = copy.deepcopy(other.promoted_pieces)
            self.player_pieces_list = copy.deepcopy(other.player_pieces_list)
        else:
            self.board = np.zeros((8, 8), dtype=np.int8)
            self.rooks_moved, self.kings_moved = [-1, -1, -1, -1], [-1, -1]
            self.current_player = 1
            self.move_list, self.pgn_str = [], []
            self.captured_pieces, self.promoted_pieces = {}, {}
            self.__set_row(0, home_row)
            self.__set_row(1, ["P"] * 8)
            self.__set_row(6, ["p"] * 8)
            self.__set_row(7, [p.lower() for p in home_row])
            self.init_player_pieces()

    def init_player_pieces(self):
        self.player_pieces_list =[{c for c in all_coords if self.is_color(c, color)} for color in (WHITE, BLACK)]

    def coord(self, coord, piece=None):
        if piece is None:
            return self.board[coord[1]][coord[0]]
        self.board[coord[1]][coord[0]] = piece

    def is_color(self, coord, color): return self.color(coord) == color

    def color(self, coord):
        piece_type = self.board[coord[1]][coord[0]]
        if piece_type == EMPTY:
            return EMPTY
        return WHITE if piece_type < 7 else BLACK

    def is_type(self, coord, piece_type): return pieces[self.coord(coord)].lower() == piece_type.lower()

    def player_pieces_of_type(self, piece_type, player):
        for coord in self.player_pieces_list[player - 1]:
            if self.coord(coord) in pieces_type_map[piece_type]:
                yield coord

    def player_pieces(self, player): return self.player_pieces_list[player - 1]

    def game_state(self):
        piece_moves = self.valid_moves_for_player(self.current_player, True)
        moves = []
        for piece in piece_moves:
            moves.extend(piece_moves[piece])
        check = self.check_check(self.current_player)
        if len(moves) == 0:
            return CHECKMATE if check else STALEMATE
        return CHECK if check else NORMAL

    def valid_moves(self):
        threats = self.compute_threat_matrix(self.current_player)
        moves = self.valid_moves_for_player(self.current_player, True, threats)
        return moves

    def valid_moves_for_player(self, player, validate=True, threats=None):
        pieces = copy.deepcopy(self.player_pieces(player))
        return {piece: list(self.valid_piece_moves(piece, validate, threats)) for piece in pieces}

    def valid_piece_moves(self, p, validate=True, threats=None):
        # TODO detect check and checkmate
        p_type = self.coord(p)
        p_type = p_type - 6 if p_type > 6 else p_type
        funcs = [lambda: [], self.king, self.queen, self.rook, self.bishop, self.knight, self.pawn]
        moves = funcs[p_type](p[0], p[1], threats) if p_type == 1 else funcs[p_type](p[0], p[1])
        if validate:
            player = self.current_player
            for move in moves: #simulate to prevent moving into check
                self.move(p, move, False, False)
                if not self.check_check(player):
                    self.__undo_last_move()
                    yield move
                else:
                    self.__undo_last_move()
        else:
            for move in moves:
                yield move

    def compute_threat_matrix(self, player, coord=None, max_threats=1000):
        threatened = np.zeros((8, 8), dtype=np.int8)
        for move in self._compute_threats(player):
            if move[2]:
                threatened[move[1]][move[0]] += 1
                if coord == move:
                    if threatened[coord[1]][coord[0]] > max_threats:
                        return threatened
        return threatened

    def _compute_threats(self, player):
        pieces = copy.deepcopy(self.player_pieces(inverse_color(player)))
        for piece in pieces:
            for move in self.valid_piece_moves(piece, False):
                if move[2]:
                    yield move
        for pawn in self.player_pieces_of_type("P", inverse_color(player)):
            for threat in self.pawn_threats(pawn[0], pawn[1]):
                yield threat

    def check_check(self, player, threats=None):
        threats = self._compute_threats(player) if threats is None else threats
        king = list(self.player_pieces_of_type("K", player))
        return (king[0][0], king[0][1], True) in threats

    def move(self, from_coord, to_coord, validate=True, pgn_gen=True):
        if validate:
            threats = self.compute_threat_matrix(self.current_player) if self.is_type(from_coord, "K") else None
            valid_moves = self.valid_piece_moves(from_coord, True, threats) if self.is_color(from_coord, self.current_player) else {}
        if not validate or to_coord in valid_moves:
            pgn_castle, pgn_promotion, file_disambiguation, rank_disambiguation = None, "", "", ""
            if self.is_type(from_coord, "K") and from_coord in king_positions:
                if to_coord in king_castle_end_positions:
                    castle_pos_index = king_castle_end_positions.index(to_coord)
                    pgn_castle = "O-O-O " if castle_pos_index == 0 or castle_pos_index == 2 else "O-O "
            to_color = self.color(to_coord)
            capture_str = "x" if to_color != EMPTY else ""
            if pgn_gen and validate:
                if pgn_castle is not None:
                    pgn = pgn_castle
                else:
                    pgn_type = pieces[self.coord(from_coord)].upper()
                    piece_type = self.coord(from_coord)
                    #TODO piece disambiguation if same type of piece can move to to_coord
                    for piece in self.__type_in_coords(self.player_pieces_list[self.current_player-1], piece_type):
                        if self.coord(piece) == piece_type and piece != from_coord:
                            for move in self.valid_piece_moves(piece):
                                if move == to_coord:
                                    if piece[0] == from_coord[0]:
                                        rank_disambiguation = str(from_coord[1] + 1)
                                    else:
                                        file_disambiguation = index_to_file(from_coord[0])
                    notation_coord = coord_to_notation(to_coord)
                    if pgn_type == "P":
                        if len(to_coord) == 4 and to_coord[3] != 6 and to_coord[3] != 12:
                            pgn_promotion = "=" + to_coord[3].upper()
                        if capture_str != "":
                            pgn = index_to_file(from_coord[0]) + capture_str + notation_coord + pgn_promotion
                        else:
                            pgn = notation_coord + pgn_promotion
                    else:
                        pgn = pgn_type + file_disambiguation + rank_disambiguation + capture_str + notation_coord

                if self.current_player == WHITE:
                    self.pgn_str.append(str(self.get_full_move_clock()) + ".")
                self.pgn_str.append(pgn)
            if self.is_type(from_coord, "R") and from_coord in rook_positions_index:
                rook_index = rook_positions_index[from_coord]
                if self.rooks_moved[rook_index] == -1:
                    self.rooks_moved[rook_index] = len(self.move_list)
            elif self.is_type(from_coord, "K") and from_coord in king_positions:
                king_index = king_positions.index(from_coord)
                if self.kings_moved[king_index] == -1:
                    self.kings_moved[king_index] = len(self.move_list)
                if to_coord in king_castle_end_positions:
                    rook_index = king_castle_end_positions_index[to_coord]
                    self.__move(rook_positions[rook_index], rook_castle_end_positions[rook_index])
                    castle_pos_index = king_castle_end_positions.index(to_coord)
            self.__move(from_coord, to_coord)
            self.move_list.append((from_coord, (to_coord[0], to_coord[1])))
            if len(to_coord) == 4:
                self.__handle_special(from_coord, to_coord)
            self.current_player = inverse_color(self.current_player)
            if pgn_gen and validate:
                state = self.game_state()
                modifier = None
                if state == CHECK:
                    modifier = "+"
                elif state == CHECKMATE:
                    modifier = "#"
                if modifier is not None:
                    self.pgn_str[-1] += modifier
        else:
            raise BadMoveException("Move is invalid")

    def __move(self, from_coord, to_coord):
        from_color = self.color(from_coord)
        to_color = self.color(to_coord)
        if to_color != EMPTY:
            captured = (to_coord[0], to_coord[1])
            self.captured_pieces[len(self.move_list)] = (self.coord(captured), captured)
            self.player_pieces_list[to_color - 1].remove(captured)
        self.player_pieces_list[from_color - 1].remove(from_coord)
        self.player_pieces_list[from_color - 1].add((to_coord[0], to_coord[1]))
        self.coord(to_coord, self.coord(from_coord))
        self.coord(from_coord, EMPTY)

    def __undo_last_move(self):
        last_move = self.move_list.pop()
        last_move_type = self
        last_move_index = len(self.move_list)
        captured = self.captured_pieces.pop(last_move_index, None)
        self.current_player = inverse_color(self.current_player)
        if self.is_type(last_move[1], "R") and last_move[0] in rook_positions:
            if self.rooks_moved[rook_positions_index[last_move[0]]] == last_move_index:
                self.rooks_moved[rook_positions_index[last_move[0]]] = -1
        elif self.is_type(last_move[1], "K") and last_move[0] in king_positions:
            if self.kings_moved[king_positions.index(last_move[0])] == last_move_index:
                self.kings_moved[king_positions.index(last_move[0])] = -1
                king_pos = (last_move[1][0], last_move[1][1], False)
                if king_pos in king_castle_end_positions: #last move was castle
                    rook_index = king_castle_end_positions_index[king_pos]
                    rook_pos = rook_castle_end_positions[rook_index]
                    self.__move((rook_pos[0], rook_pos[1]), rook_positions[rook_index])
        elif last_move_index in self.promoted_pieces:
            self.coord(last_move[1], 6 if self.current_player == WHITE else 12)
            self.promoted_pieces.pop(last_move_index)
        self.__move(last_move[1], last_move[0])
        if captured is not None:
            self.coord(captured[1], captured[0])
            self.player_pieces_list[self.color(captured[1]) - 1].add(captured[1])

    def __handle_special(self, from_coord, to_coord):
        if to_coord[3] == 6 or to_coord[3] == 12: #en pessant
            captured = (to_coord[0], from_coord[1])
            captured_color = self.color(captured)
            self.captured_pieces[len(self.move_list) - 1] = (self.coord(captured), captured)
            self.coord(captured, EMPTY)
            self.player_pieces_list[captured_color - 1].remove(captured)
        else: #promotion
            promotion_type = to_coord[3]
            if promotion_type.upper() in promotion_candidates and self.is_type(to_coord, "P"):
                if self.current_player == WHITE and to_coord[1] == 7:
                    self.coord(to_coord, pieces_index[promotion_type.upper()])
                elif self.current_player == BLACK and to_coord[1] == 0:
                    self.coord(to_coord, pieces_index[promotion_type.lower()])
                else:
                    raise BadPromotionException("Cannot promote from this position")
                self.promoted_pieces[len(self.move_list)-1] = (self.coord(to_coord), to_coord)
            else:
                raise BadPromotionException("Invalid promotion")

    def pawn_threats(self, f, r):
        color = self.color((f, r))
        for threat in self.__warps([], (f, r), pawn_capture_warps[color - 1], (color,)):
            yield threat

    def pawn(self, f, r):
        color = self.color((f, r))
        warps = [[(0, 1), (0, 2)] if r == 1 and self.is_color((f, r + 1), EMPTY) else [(0, 1)]]
        warps.append([(0, -1), (0, -2)] if r == 6 and self.is_color((f, r - 1), EMPTY) else [(0, -1)])
        moves = self.__warps([], (f, r), warps[color - 1], (WHITE, BLACK), False)
        for move in self.__warps(moves, (f, r), pawn_capture_warps[color - 1], (EMPTY, color)):
            if color == WHITE and move[1] == 7:
                for promotion in promotion_candidates:
                    yield (move[0], move[1], move[2], promotion)
            elif color == BLACK and move[1] == 0:
                for promotion in promotion_candidates:
                    yield (move[0], move[1], move[2], promotion.lower())
            else:
                yield move
        if len(self.move_list) > 0: #en pessant
            last_move = self.move_list[-1]
            if self.is_type(last_move[1], "P") and self.is_color(last_move[1], inverse_color(color)):
                if abs(last_move[1][1] - last_move[0][1]) == 2 and abs(last_move[0][0] - f) == 1 and last_move[1][1] == r:
                    yield (last_move[0][0], r + 1, False, self.coord((f, r)))

    def rook(self, f, r): return self.orthogonal([], f, r)

    def bishop(self, f, r): return self.diagonal([], f, r)

    def knight(self, f, r): return self.__warps([], (f, r), knight_warps, (self.color((f, r)),))

    def queen(self, f, r): return self.orthogonal(self.diagonal([], f, r), f, r)

    def king(self, f, r, threats=None):
        color = self.color((f, r))
        castle_moves = []
        if self.kings_moved[color - 1] == -1:
            if self.rooks_moved[0 if color == WHITE else 2] == -1 and self.positions_clear([(1, r), (2, r), (3, r)], threats):
                castle_moves.append((2, r, False))
            if self.rooks_moved[1 if color == WHITE else 3] == -1 and self.positions_clear([(5, r), (6, r)], threats):
                castle_moves.append((6, r, False))
        for move in self.__warps(castle_moves, (f, r), king_warps, (color,)):
            yield move

    def positions_clear(self, coords, threats=None):
        for coord in coords:
            status = 0 if threats is None else threats[coord[1]][coord[0]]
            if self.coord(coord) != 0 or status != 0:
                return False
        return True

    def __warps(self, moves, coord, relative_warps, excluded, threat=True):
        for move in moves:
            yield move
        for w in relative_warps:
            warp = (coord[0] + w[0], coord[1] + w[1], threat)
            if in_range(warp) and self.color(warp) not in excluded:
                yield warp

    def orthogonal(self, moves, f, r): return self.__vectors(moves, f, r, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def diagonal(self, moves, f, r): return self.__vectors(moves, f, r, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

    def __vectors(self, moves, f, r, offsets_list):
        for move in moves:
            yield move
        for offset in offsets_list:
            for move in self.__vector(f, r, offset):
                yield move

    def __vector(self, f, r, offset):
        color = self.color((f, r))
        inv_color = inverse_color(color)
        coord = (f + offset[1], r + offset[0], True)
        while in_range(coord) and self.color(coord) in (inv_color, EMPTY):
            yield coord
            if self.color(coord) == inv_color:
                break
            coord = (offset[1] + coord[0], offset[0] + coord[1], coord[2])

    def __type_in_coords(self, coords, type):
        for coord in coords:
            if self.coord(coord) == type:
                yield coord

    def __set_row(self, row, row_pieces):
        map2(lambda col: self.coord((col, row), pieces_index[row_pieces[col]]), [col for col in range(SIZE)])

    def __str__(self):
        piece_arr = [pieces_ascii[self.coord((coord[1], SIZE - coord[0] - 1))] for coord in all_coords]
        return "".join([" ".join(piece_arr[i*SIZE:i*SIZE+SIZE])+"\n" for i in range(SIZE)])

    def fen(self):
        hash = []
        for i, coord in enumerate(all_coords):
            p_type = self.coord((coord[1], SIZE - coord[0] - 1))
            if i % 8 == 0 and i > 0:
                hash.append("/")
            if p_type == EMPTY:
                if len(hash) > 0 and hash[-1] in ("1", "2", "3", "4", "5", "6", "7", "8"):
                    hash[-1] = str(int(hash[-1]) + 1)
                else:
                    hash.append("1")
            else:
                hash.append(pieces[p_type])
        hash.append(" w " if self.current_player == WHITE else " b ")

        hash_len = len(hash)
        if self.kings_moved[0] == -1:
            if self.rooks_moved[0] == -1:
                hash.append("K")
            if self.rooks_moved[1] == -1:
                hash.append("Q")
        if self.kings_moved[1] == -1:
            if self.rooks_moved[2] == -1:
                hash.append("k")
            if self.rooks_moved[3] == -1:
                hash.append("q")
        if len(hash) == hash_len: #nothing new appeneded for castling
            hash.append("-")
        if len(self.move_list) > 0:
            last_move = self.move_list[-1]
            if self.is_type(last_move[1], "P") and abs(last_move[1][1] - last_move[0][1]) == 2: #en pessant target
                behind_rank = last_move[1][1] - (-1 if self.current_player == WHITE else 1) #reversed for opponents pawn
                hash.append(" " + coord_to_notation((last_move[1][0], behind_rank)) + " ")
            else:
                hash.append(" - ")
        else:
            hash.append(" - ")
        hash.append(str(self.get_half_move_clock()))
        full_moves = self.get_full_move_clock()
        hash.append(" " + str(full_moves))
        return "".join(hash)

    def get_full_move_clock(self):
        return math.floor(len(self.move_list) / 2) + 1

    def get_half_move_clock(self):
        move_index = len(self.move_list)
        if move_index > 0:
            last_cap_or_pawn = move_index
            while last_cap_or_pawn:
                if (last_cap_or_pawn - 1) in self.captured_pieces:
                    break
                if self.is_type(self.move_list[last_cap_or_pawn - 1][1], "P"):
                    break
                last_cap_or_pawn -= 1
            return move_index - last_cap_or_pawn
        else:
            return 0

    def pgn(self):
        return " ".join(self.pgn_str)
