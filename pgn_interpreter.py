import logging
from lark import Visitor
from chess import file_to_index, Chess

WHITE = 1
BLACK = 2

logging.basicConfig(level=logging.WARN)

def rank_file_to_coord(to_rank_file):
    return (file_to_index(to_rank_file[0]), int(to_rank_file[1]) - 1)

class ChessInterpreter():

    def __init__(self, board):
        self.board = board
        self.player = WHITE
        self.turn_number = 0
        self.white_piece = None
        self.black_piece = None

    def execute(self, tree):
        print(self.board)
        for turn in tree.children:
            self.turn(turn)

    def turn(self, tree):
        self.turn_number = int(tree.children[0])
        print("Turn: " + str(self.turn_number))
        self.move(tree.children[1])
        if len(tree.children) == 3:
            self.move(tree.children[2])

    def move(self, tree):
        if tree.children[0].data == "rank":
            self.set_piece("pawn")
            to_rank_file = self.coord(tree.children[2])
            to_coord = rank_file_to_coord(to_rank_file)
            piece = self.set_piece("p")
        elif tree.children[0].data == "coord":
            self.set_piece("pawn")
            to_rank_file = self.coord(tree.children[0])
            to_coord = rank_file_to_coord(to_rank_file)
            piece = self.set_piece("p")
        else:
            piece = self.set_piece(tree.children[0].data)
            if tree.children[1].data == "capture":
                to_rank_file = self.coord(tree.children[2])
            else:
                to_rank_file = self.coord(tree.children[1])
            to_coord = rank_file_to_coord(to_rank_file)
        of_type = self.board.get_current_player_pieces_of_type(piece)
        logging.debug("Looking for piece that can move to " + str(to_coord))
        logging.debug("Possible options are: " + str(of_type))
        for piece in of_type:
            moves = self.board.valid_piece_moves(piece[0], piece[1])
            for move in moves:
                if move == to_coord:
                    from_coord = piece
        if self.player == WHITE:
            logging.debug("White moving: " + self.white_piece)
            self.player = BLACK
        else:
            logging.debug("Black moving: " + self.black_piece)
            self.player = WHITE

        try:
            self.board.move(from_coord, to_coord)
            print(self.board)
        except:
            raise Exception("No valid move found with that specification.")

    def coord(self, tree):
        file = self.rank(tree.children[0])
        rank = self.file(tree.children[1])
        coord = (file, rank)
        return coord

    def rank(self, tree):
        return str(tree.children[0])

    def file(self, tree):
        return str(tree.children[0])

    def set_piece(self, piece):
        if self.player == WHITE:
            self.white_piece = str(piece).upper()
            return self.white_piece
        else:
            self.black_piece = str(piece).upper()
            return self.black_piece

