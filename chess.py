import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
WHITE = 1
BLACK = 2

increment = lambda x: x + 1
decrement = lambda x: x - 1
nothing = lambda x: x
file_to_index = lambda file: ord(file) - 97

class Chess:

    def __init__(self):
        self.current_player = 1
        self.move_list = []
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.set_row(0, home_row)
        self.set_row(1, ["P"] * 8)
        self.set_row(6, ["p"] * 8)
        self.set_row(7, [p.lower() for p in home_row])

    def get_coord(self, coord):
        return self.board[coord[1]][coord[0]]

    def set_coord(self, coord, piece):
        self.board[coord[1]][coord[0]] = piece

    def move(self, from_coord, to_coord):
        #coordinates are always in the format (file, rank)
        is_valid = ((from_coord, to_coord) in self.valid_moves())
        if is_valid:
            #print("Moving: " + pieces_ascii[from_piece])
            self.set_coord(to_coord, self.get_coord(from_coord))
            self.set_coord(from_coord, 0)
            if self.current_player == WHITE:
                self.current_player = BLACK
            else:
                self.current_player = WHITE
        else:
            raise Exception("Move is invalid")

    def valid_moves(self):
        moves = []
        player_pieces = self.get_current_player_pieces()
        for piece in player_pieces:
            piece_moves = self.valid_piece_moves(piece[0], piece[1])
            for move in piece_moves:
                moves.append((piece, move))
        return moves

    def get_current_player_pieces_of_type(self, piece_type):
        player_pieces = self.get_current_player_pieces()
        of_type = []
        for piece in player_pieces:
            cell = self.get_coord(piece)
            if cell == pieces.index(piece_type) or cell == pieces.index(piece_type.lower()):
                of_type.append(piece)
        return of_type

    def get_current_player_pieces(self):
        player_pieces = []
        for row in range(SIZE):
            for col in range(SIZE):
                if self.get_piece_color(col, row) == self.current_player:
                    player_pieces.append((col, row))
        return player_pieces

    def valid_piece_moves(self, file, rank):
        # TODO promotion
        # TODO current player cannot make a move that puts their king in check
        # TODO castling
        piece_type = self.board[rank][file]
        move_funcs = [lambda: [], self.king_moves, self.queen_moves, self.rook_moves, self.bishop_moves, self.knight_moves, self.pawn_moves]
        if piece_type > 6:
            piece_type -= 6
        moves = move_funcs[piece_type](file, rank)
        return moves

    def pawn_moves(self, file, rank):
        moves = []
        # TODO en pessant
        color = self.get_piece_color(file, rank)
        first_move = (color == WHITE and rank == 1) or (color == BLACK and rank == 6)
        if color == WHITE:
            warps = [(0, 1), (0, 2)] if first_move else [(0, 1)]
            capture_warps = [(-1, 1), (1, 1)]
        elif color == BLACK:
            warps = [(0, -1), (0, -2)] if first_move else [(0, -1)]
            capture_warps = [(-1, -1), (1, -1)]
        moves.extend(self.apply_warps(file, rank, (file, rank), warps, (1, 2)))
        moves.extend(self.apply_warps(file, rank, (file, rank), capture_warps, (0, color)))
        return moves

    def rook_moves(self, file, rank):
        moves = self.valid_vertical_moves(file, rank)
        moves.extend(self.valid_horizontal_moves(file, rank))
        return moves

    def bishop_moves(self, file, rank):
        return self.valid_diagonal_moves(file, rank)

    def knight_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        return self.apply_warps(file, rank, (file, rank), warps, (color,))

    def queen_moves(self, file, rank):
        moves = self.valid_diagonal_moves(file, rank)
        moves.extend(self.valid_vertical_moves(file, rank))
        moves.extend(self.valid_horizontal_moves(file, rank))
        return moves

    def king_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        return self.apply_warps(file, rank, (file, rank), warps, (color,))

    def apply_warps(self, file, rank, original, warps, excluded_colors):
        moves = []
        for warp in warps:
            new_file = original[0] + warp[0]
            new_rank = original[1] + warp[1]
            if new_file in range(SIZE) and new_rank in range(SIZE):
                if self.get_piece_color(new_file, new_rank) not in excluded_colors:
                    moves.append((new_file, new_rank))
        return moves

    def valid_vertical_moves(self, file, rank):
        moves = []
        self.valid_moves_lambda(moves, rank, file, increment, nothing)
        self.valid_moves_lambda(moves, rank, file, decrement, nothing)
        return moves

    def valid_horizontal_moves(self, file, rank):
        moves = []
        self.valid_moves_lambda(moves, rank, file, nothing, increment)
        self.valid_moves_lambda(moves, rank, file, nothing, decrement)
        return moves

    def valid_diagonal_moves(self, file, rank):
        moves = []
        self.valid_moves_lambda(moves, rank, file, increment, increment)
        self.valid_moves_lambda(moves, rank, file, decrement, decrement)
        self.valid_moves_lambda(moves, rank, file, increment, decrement)
        self.valid_moves_lambda(moves, rank, file, decrement, increment)
        return moves

    def valid_moves_lambda(self, moves, rank, file, rank_func, file_func):
        color = self.get_piece_color(file, rank)
        on_rank = rank_func(rank)
        on_file = file_func(file)
        while on_rank in range(SIZE) and on_file in range(SIZE):
            move_color = self.get_piece_color(on_file, on_rank)
            if move_color != 0:
                if move_color != color:
                    moves.append((on_file, on_rank))
                return
            moves.append((on_file, on_rank))
            on_rank = rank_func(on_rank)
            on_file = file_func(on_file)

    def get_piece_color(self, file, rank):
        sep_index = pieces.index("k")
        if self.board[rank][file] == 0:
            return 0  # empty
        elif self.board[rank][file] < sep_index:
            return WHITE
        return BLACK

    def set_row(self, row, row_pieces):
        for col in range(SIZE):
            self.board[row][col] = pieces.index(row_pieces[col])

    def __str__(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                piece = self.board[SIZE-row-1][col]
                board_str += pieces_ascii[piece] + " "
            board_str += "\n"
        return board_str

    def hash(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                board_str += pieces[self.board[SIZE-row-1][col]]
        return board_str
