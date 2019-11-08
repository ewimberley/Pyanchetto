import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
rook_positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
king_positions = [(4, 0), (4, 7)]
king_castle_end_positions = [(2, 0), (6, 0), (2, 7), (6, 7)]
rook_castle_end_positions = [(3, 0), (5, 0), (3, 7), (5, 7)]
EMPTY = 0
WHITE = 1
BLACK = 2

def increment(x): return x + 1
def decrement(x): return x - 1
def nothing(x): return x
def file_to_index(file): return ord(file) - 97

class Chess:

    def __init__(self):
        self.current_player = 1
        self.move_list = []
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.rooks_moved = np.zeros(4, dtype=np.bool_)
        self.kings_moved = np.zeros(2, dtype=np.bool_)
        self.__set_row(0, home_row)
        self.__set_row(1, ["P"] * 8)
        self.__set_row(6, ["p"] * 8)
        self.__set_row(7, [p.lower() for p in home_row])

    def get_coord(self, coord): return self.board[coord[1]][coord[0]]

    def set_coord(self, coord, piece): self.board[coord[1]][coord[0]] = piece

    def is_color(self, coord, color): return self.get_piece_color(coord[0], coord[1]) == color

    def move(self, from_coord, to_coord):
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
            if self.current_player == WHITE:
                self.current_player = BLACK
            else:
                self.current_player = WHITE
        else:
            raise Exception("Move is invalid")

    def __move(self, from_coord, to_coord):
        self.set_coord(to_coord, self.get_coord(from_coord))
        self.set_coord(from_coord, EMPTY)

    def coord_is_type(self, coord, piece_type):
        return pieces[self.get_coord(coord)].lower() == piece_type.lower()

    def valid_moves(self):
        moves = []
        for piece in self.get_current_player_pieces():
            piece_moves = self.valid_piece_moves(piece[0], piece[1])
            for move in piece_moves:
                moves.append((piece, move))
        return moves

    def get_current_player_pieces_of_type(self, piece_type):
        of_type = []
        for piece in self.get_current_player_pieces():
            if self.get_coord(piece) in (pieces.index(piece_type), pieces.index(piece_type.lower())):
                of_type.append(piece)
        return of_type

    def get_current_player_pieces(self):
        player_pieces = []
        for row in range(SIZE):
            for col in range(SIZE):
                if self.is_color((col, row), self.current_player):
                    player_pieces.append((col, row))
        return player_pieces

    def valid_piece_moves(self, file, rank):
        # TODO promotion
        # TODO current player cannot make a move that puts their king in check
        # TODO capturing the king is not a valid move
        # TODO detect check and checkmate
        piece_type = self.board[rank][file]
        move_funcs = [lambda: [], self.king_moves, self.queen_moves, self.rook_moves, self.bishop_moves, self.knight_moves, self.pawn_moves]
        if piece_type > 6:
            piece_type -= 6
        moves = move_funcs[piece_type](file, rank)
        return moves

    def pawn_moves(self, file, rank):
        # TODO en pessant
        color = self.get_piece_color(file, rank)
        first_move = (color == WHITE and rank == 1) or (color == BLACK and rank == 6)
        if color == WHITE:
            warps = [(0, 1), (0, 2)] if first_move and self.is_color((file, rank + 1), EMPTY) else [(0, 1)]
            capture_warps = [(-1, 1), (1, 1)]
        elif color == BLACK:
            warps = [(0, -1), (0, -2)] if first_move and self.is_color((file, rank - 1), EMPTY) else [(0, -1)]
            capture_warps = [(-1, -1), (1, -1)]
        moves = self.apply_warps([], file, rank, (file, rank), warps, (1, 2))
        return self.apply_warps(moves, file, rank, (file, rank), capture_warps, (EMPTY, color))

    def rook_moves(self, file, rank):
        moves = self.valid_vertical_moves([], file, rank)
        self.valid_horizontal_moves(moves, file, rank)
        return moves

    def bishop_moves(self, file, rank): return self.valid_diagonal_moves([], file, rank)

    def knight_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        return self.apply_warps([], file, rank, (file, rank), warps, (color,))

    def queen_moves(self, file, rank):
        moves = self.valid_diagonal_moves([], file, rank)
        self.valid_vertical_moves(moves, file, rank)
        self.valid_horizontal_moves(moves, file, rank)
        return moves

    def king_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        castle_moves = []
        if not self.kings_moved[color-1]:
            if not self.rooks_moved[0 if color == WHITE else 2] and self.positions_clear([(1, rank), (2, rank), (3, rank)]):
                castle_moves.append((2, rank))
            if not self.rooks_moved[1 if color == WHITE else 3] and self.positions_clear([(5, rank), (6, rank)]):
                castle_moves.append((6, rank))
        return self.apply_warps(castle_moves, file, rank, (file, rank), warps, (color,))

    def positions_clear(self, coords):
        for coord in coords:
            if self.get_coord(coord) != 0:
                return False
        return True

    def apply_warps(self, moves, file, rank, original, warps, excluded_colors):
        for warp in warps:
            new_coord = (original[0] + warp[0], original[1] + warp[1])
            if new_coord[0] in range(SIZE) and new_coord[1] in range(SIZE):
                if self.get_piece_color(new_coord[0], new_coord[1]) not in excluded_colors:
                    moves.append(new_coord)
        return moves

    def valid_vertical_moves(self, moves, file, rank):
        self.__valid_moves_lambda(moves, rank, file, increment, nothing)
        self.__valid_moves_lambda(moves, rank, file, decrement, nothing)
        return moves

    def valid_horizontal_moves(self, moves, file, rank):
        self.__valid_moves_lambda(moves, rank, file, nothing, increment)
        self.__valid_moves_lambda(moves, rank, file, nothing, decrement)
        return moves

    def valid_diagonal_moves(self, moves, file, rank):
        self.__valid_moves_lambda(moves, rank, file, increment, increment)
        self.__valid_moves_lambda(moves, rank, file, decrement, decrement)
        self.__valid_moves_lambda(moves, rank, file, increment, decrement)
        self.__valid_moves_lambda(moves, rank, file, decrement, increment)
        return moves

    def __valid_moves_lambda(self, moves, rank, file, rank_func, file_func):
        color = self.get_piece_color(file, rank)
        on_coord = (file_func(file), rank_func(rank))
        while on_coord[0] in range(SIZE) and on_coord[1] in range(SIZE):
            move_color = self.get_piece_color(on_coord[0], on_coord[1])
            if move_color != EMPTY:
                if move_color != color:
                    moves.append(on_coord)
                return
            moves.append(on_coord)
            on_coord = (file_func(on_coord[0]), rank_func(on_coord[1]))

    def get_piece_color(self, file, rank):
        if self.board[rank][file] == EMPTY:
            return EMPTY
        elif self.board[rank][file] < pieces.index("k"):
            return WHITE
        return BLACK

    def __set_row(self, row, row_pieces):
        for col in range(SIZE):
            self.board[row][col] = pieces.index(row_pieces[col])

    def __str__(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                board_str += pieces_ascii[self.get_coord((col, SIZE-row-1))] + " "
            board_str += "\n"
        return board_str

    def hash(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                board_str += pieces[self.get_coord((col, SIZE-row-1))]
        return board_str
