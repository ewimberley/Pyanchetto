import logging
from lark import Visitor
from chess import file_to_index, Chess, BadMoveException

WHITE = 1
BLACK = 2

logging.basicConfig(level=logging.DEBUG)

def rank_file_to_coord(to_rank_file):
    return (file_to_index(to_rank_file[0]), int(to_rank_file[1]) - 1)

class ChessInterpreter():

    def __init__(self, board):
        self.board = board
        self.turn_number = 0
        self.verbose = False

    def execute(self, tree, verbose):
        #TODO set logging level based on verbose
        self.verbose = verbose
        self.pgn(tree.children[0])

    def pgn(self, tree):
        if self.verbose:
            print(self.board)
        for child in tree.children:
            if child.data == "turn":
                self.turn(child)

    def turn(self, tree):
        self.turn_number = int(tree.children[0])
        logging.info("Turn: " + str(self.turn_number))
        self.move(tree.children[1])
        if len(tree.children) == 3:
            self.move(tree.children[2])

    def move(self, tree):
        required_file = -1
        if tree.children[0].data in ("king_side_castle", "queen_side_castle"):
            piece, self.to_coord = self.castle(tree.children[0])
        elif tree.children[0].data == "file":
            required_file = file_to_index(self.file(tree.children[0]))
            self.to_coord = self.coord(tree.children[2])
            self.set_piece("p")
        elif tree.children[0].data == "coord":
            self.to_coord = self.coord(tree.children[0])
            self.set_piece("p")
        else:
            self.set_piece(tree.children[0].data)
            if tree.children[1].data == "capture":
                self.to_coord = self.coord(tree.children[2])
            else:
                self.to_coord = self.coord(tree.children[1])
        of_type = self.board.get_current_player_pieces_of_type(self.piece)
        logging.debug("Looking for piece that can move to " + str(self.to_coord))
        logging.debug("Possible options are: " + str(of_type))
        for piece in of_type:
            if required_file != -1:
                if piece[0] != required_file:
                    continue
            moves = self.board.valid_piece_moves(piece[0], piece[1])
            for move in moves:
                if move == self.to_coord:
                    from_coord = piece
        try:
            self.board.move(from_coord, self.to_coord)
            logging.info("\n" + str(self.board))
        except BadMoveException:
            raise Exception("No valid move found with that specification.")

    def coord(self, tree):
        file = self.rank(tree.children[0])
        rank = self.file(tree.children[1])
        return rank_file_to_coord((file, rank))

    def rank(self, tree):
        return str(tree.children[0])

    def file(self, tree):
        return str(tree.children[0])

    def castle(self, tree):
        piece = self.set_piece("k")
        if tree.data == "king_side_castle":
            to_coord = (6, 0) if self.board.current_player == WHITE else (6, 7)
        elif tree.data == "queen_side_castle":
            to_coord = (2, 0) if self.board.current_player == WHITE else (2, 7)
        return piece, to_coord

    def set_piece(self, piece):
        self.piece = str(piece).upper()
