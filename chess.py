import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]

increment = lambda x: x + 1
decrement = lambda x: x - 1
nothing = lambda x: x


def file_to_index(file):
    return ord(file) - 97

class Chess:

    def __init__(self):
        self.current_player = 1
        self.move_list = []
        # TODO colors are reversed
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.set_row(0, home_row)
        self.set_row(1, ["P"] * 8)
        self.set_row(6, ["p"] * 8)
        self.set_row(7, [p.lower() for p in home_row])

    def move(self, from_coord, to_coord):
        """coordinates are in format (file, rank)"""
        from_file = from_coord[0]
        from_rank = from_coord[1]
        from_piece = self.board[from_rank][from_file]
        to_file = to_coord[0]
        to_rank = to_coord[1]
        to_piece = self.board[to_rank][to_file]
        valid_moves = self.valid_moves()
        is_valid = False
        for valid in valid_moves:
            if valid[0][0] == from_file and valid[0][1] == from_rank:
                if valid[1][0] == to_file and valid[1][1] == to_rank:
                    is_valid = True
        if is_valid:
            #print("Moving: " + pieces_ascii[from_piece])
            self.board[to_rank][to_file] = self.board[from_rank][from_file]
            self.board[from_rank][from_file] = 0
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
        else:
            raise Exception("Move is invalid")

    def valid_moves(self):
        # TODO king cannot move into check
        moves = []
        player_pieces = self.get_current_player_pieces()
        for piece in player_pieces:
            piece_moves = self.valid_piece_moves(piece[0], piece[1])
            for move in piece_moves:
                moves.append((piece, move))
        return moves

    def get_current_player_pieces_of_type(self, type):
        player_pieces = self.get_current_player_pieces()
        of_type = []
        for piece in player_pieces:
            cell = self.board[piece[1]][piece[0]]
            if cell == pieces.index(type) or cell == pieces.index(type.lower()):
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
        piece_type = self.board[rank][file]
        if piece_type == 1 or piece_type == 7:
            return self.valid_king_moves(file, rank)
        elif piece_type == 2 or piece_type == 8:
            return self.valid_queen_moves(file, rank)
        elif piece_type == 3 or piece_type == 9:
            return self.valid_rook_moves(file, rank)
        elif piece_type == 4 or piece_type == 10:
            return self.valid_bishop_moves(file, rank)
        elif piece_type == 5 or piece_type == 11:
            return self.valid_knight_moves(file, rank)
        elif piece_type == 6 or piece_type == 12:
            return self.valid_pawn_moves(file, rank)

    def valid_pawn_moves(self, file, rank):
        moves = []
        # TODO en pessant
        # TODO promotion
        color = self.get_piece_color(file, rank)
        first_move = (color == 1 and rank == 1) or (color == 2 and rank == 6)
        if color == 1:
            if (rank + 1) in range(SIZE) and self.board[rank + 1][file] == 0:
                moves.append((file, rank + 1))
                if first_move and (rank + 2) in range(SIZE) and self.board[rank + 2][file] == 0:
                    moves.append((file, rank + 2))
            capture_warps = [(-1, 1), (1, 1)]
            moves.extend(self.apply_capture_warps(2, file, rank, (file, rank), capture_warps))
        elif color == 2:
            if (rank - 1) in range(SIZE) and self.board[rank - 1][file] == 0:
                moves.append((file, rank - 1))
                if first_move and (rank - 2) in range(SIZE) and self.board[rank - 2][file] == 0:
                    moves.append((file, rank - 2))
            capture_warps = [(-1, -1), (1, -1)]
            moves.extend(self.apply_capture_warps(1, file, rank, (file,rank), capture_warps))
        return moves

    def valid_rook_moves(self, file, rank):
        moves = self.valid_vertical_moves(file, rank)
        moves.extend(self.valid_horizontal_moves(file, rank))
        return moves

    def valid_bishop_moves(self, file, rank):
        moves = self.valid_diagonal_moves(file, rank)
        return moves

    def valid_knight_moves(self, file, rank):
        original = (file, rank)
        warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        return self.apply_warps(file, rank, original, warps)

    def valid_queen_moves(self, file, rank):
        moves = self.valid_diagonal_moves(file, rank)
        moves.extend(self.valid_vertical_moves(file, rank))
        moves.extend(self.valid_horizontal_moves(file, rank))
        return moves

    def valid_king_moves(self, file, rank):
        original = (file, rank)
        warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        return self.apply_warps(file, rank, original, warps)

    def apply_warps(self, file, rank, original, warps):
        moves = []
        for warp in warps:
            after_warp = (original[0] + warp[0], original[1] + warp[1])
            self.add_if_valid_warp_move(moves, file, rank, after_warp)
        return moves

    def add_if_valid_warp_move(self, moves, file, rank, new_position):
        new_file = new_position[0]
        new_rank = new_position[1]
        color = self.get_piece_color(file, rank)
        if new_file in range(SIZE) and new_rank in range(SIZE):
            if self.get_piece_color(new_file, new_rank) != color:
                moves.append((new_file, new_rank))

    def apply_capture_warps(self, other_player, file, rank, original, warps):
        moves = []
        for warp in warps:
            after_warp = (original[0] + warp[0], original[1] + warp[1])
            self.add_if_valid_capture_warp_move(other_player, moves, file, rank, after_warp)
        return moves

    def add_if_valid_capture_warp_move(self, other_player, moves, file, rank, new_position):
        new_file = new_position[0]
        new_rank = new_position[1]
        if new_file in range(SIZE) and new_rank in range(SIZE):
            if self.get_piece_color(new_file, new_rank) == other_player:
                moves.append((new_file, new_rank))

    def valid_vertical_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        moves = []
        self.valid_adjacent_moves_lambda(moves, rank, file, increment, nothing)
        self.valid_adjacent_moves_lambda(moves, rank, file, decrement, nothing)
        return moves

    def valid_horizontal_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        moves = []
        self.valid_adjacent_moves_lambda(moves, rank, file, nothing, increment)
        self.valid_adjacent_moves_lambda(moves, rank, file, nothing, decrement)
        return moves

    def valid_diagonal_moves(self, file, rank):
        color = self.get_piece_color(file, rank)
        moves = []
        self.valid_adjacent_moves_lambda(moves, rank, file, increment, increment)
        self.valid_adjacent_moves_lambda(moves, rank, file, decrement, decrement)
        self.valid_adjacent_moves_lambda(moves, rank, file, increment, decrement)
        self.valid_adjacent_moves_lambda(moves, rank, file, decrement, increment)
        return moves

    def valid_adjacent_moves_lambda(self, moves, rank, file, rank_func, file_func):
        color = self.get_piece_color(file, rank)
        on_rank = rank_func(rank)
        on_file = file_func(file)
        while on_rank in range(SIZE) and on_file in range(SIZE):
            move_color = self.get_piece_color(on_file, on_rank)
            if move_color != 0:
                if move_color == color:
                    return
                else:
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
            return 1  # white
        else:
            return 2  # black

    def set_row(self, row, row_pieces):
        for col in range(SIZE):
            piece = row_pieces[col]
            self.board[row][col] = pieces.index(piece)

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
                board_str += pieces[self.board[row][col]]
        return board_str
