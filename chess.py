import numpy as np

SIZE = 8
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_ascii = (".", "♚", "♛", "♜", "♝", "♞", "♟", "♔", "♕", "♖", "♗", "♘", "♙")

class Chess:

    def __init__(self):
        self.move_list = []
        self.board = np.zeros((8,8), dtype=np.int8)
        home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        self.fill_row(1, "p")
        self.set_row(0, [p.lower() for p in home_row])
        self.fill_row(6, "P")
        self.set_row(7, home_row)

    def set_row(self, row, row_pieces):
        for col in range(SIZE):
            piece = row_pieces[col]
            self.board[row][col] = pieces.index(piece)

    def fill_row(self, row, piece):
        for col in range(SIZE):
            self.board[row][col] = pieces.index(piece)

    def move(self, from_coord, to_coord):
        """coordinates are in format (file, rank)"""
        from_file = self.file_to_index(from_coord[0])
        from_rank = SIZE - from_coord[1] - 1
        from_piece = self.board[from_rank][from_file]
        print("Moving: " + pieces_ascii[from_piece])
        to_file = self.file_to_index(to_coord[0])
        to_rank = SIZE - to_coord[1] - 1
        to_piece = self.board[to_rank][to_file]
        #TODO check move is valid
        self.board[to_rank][to_file] = self.board[from_rank][from_file]
        self.board[from_rank][from_file] = 0

    def file_to_index(self, file):
        return ord(file) - 97

    def __str__(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                piece = self.board[row][col]
                board_str += pieces_ascii[piece] + " "
            board_str += "\n"
        return board_str

    def hash(self):
        board_str = ""
        for row in range(SIZE):
            for col in range(SIZE):
                board_str += pieces[self.board[row][col]]
        return board_str