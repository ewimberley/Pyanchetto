import logging
from deepfianchetto.chess import rank_file_to_coord, file_to_index

WHITE = 1
BLACK = 2

def child_index_is_type(tree, index, type):
    return tree.children[index].data == type

class ChessInterpreter():

    def __init__(self, board):
        self.board = board
        self.turn_number = 0
        self.verbose = False

    def execute(self, tree, verbose):
        #TODO set logging level based on verbose
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARN)
        self.pgn(tree.children[0])

    def pgn(self, tree):
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
        required_rank = -1
        threaten = True
        self.promotion_type = None
        if tree.children[0].data in ("king_side_castle", "queen_side_castle"):
            piece, self.to_coord = self.castle(tree.children[0])
        elif child_index_is_type(tree, 1, "disambiguation"):
            self.set_piece(tree.children[0].data)
            required_file, required_rank = self.disambiguation(tree.children[1])
            if tree.children[2].data == "capture":
                self.to_coord = self.coord(tree.children[3])
            else:
                self.to_coord = self.coord(tree.children[2])
        elif child_index_is_type(tree, 0, "file"):
            required_file = file_to_index(self.file(tree.children[0]))
            self.to_coord = self.coord(tree.children[2])
            self.set_piece("p")
            if child_index_is_type(tree, 1, "promotion"):
                self.promotion(tree)
        elif child_index_is_type(tree, 0, "coord"):
            self.to_coord = self.coord(tree.children[0])
            self.set_piece("p")
            if child_index_is_type(tree, 1, "promotion"):
                self.promotion(tree)
        else:
            self.set_piece(tree.children[0].data)
            if tree.children[1].data == "capture":
                self.to_coord = self.coord(tree.children[2])
            else:
                self.to_coord = self.coord(tree.children[1])
        from_coord, threaten, special = self.find_piece_for_move(required_file, required_rank, threaten)
        if self.promotion_type is not None:
            self.to_coord = (self.to_coord[0], self.to_coord[1], threaten, self.promotion_type)
        else:
            if special is not None:
                self.to_coord = (self.to_coord[0], self.to_coord[1], threaten, special)
            else:
                self.to_coord = (self.to_coord[0], self.to_coord[1], threaten)
        try:
            logging.debug("Player " + str(self.board.current_player) + " moving " + self.piece + " to " + str(self.to_coord))
            self.board.move(from_coord, self.to_coord)
            logging.info("\n" + str(self.board))
        except Exception as e:
            logging.exception("Failed to apply move.")
            raise e

    def find_piece_for_move(self, required_file, required_rank, threaten):
        of_type = self.board.player_pieces_of_type(self.piece, self.board.current_player)
        logging.debug("Looking for a " + str(self.piece) + " that can move to " + str(self.to_coord))
        logging.debug("Possible options are: " + str(of_type))
        for piece in of_type:
            if required_file != -1:
                if piece[0] != required_file:
                    continue
            if required_rank != -1:
                if piece[1] != required_rank:
                    continue
            for move in self.board.valid_piece_moves(piece):
                if move[0] == self.to_coord[0] and move[1] == self.to_coord[1]:
                    from_coord = piece
                    threaten = move[2]
                    special = None
                    if len(move) == 4:
                        special = move[3]
                    return from_coord, threaten, special
        return None, None

    def coord(self, tree):
        file = self.rank(tree.children[0])
        rank = self.file(tree.children[1])
        return rank_file_to_coord((file, rank))

    def rank(self, tree):
        return str(tree.children[0])

    def file(self, tree):
        return str(tree.children[0])

    def disambiguation(self, tree):
        required_file = -1
        required_rank = -1
        if child_index_is_type(tree, 0, "file"):
            required_file = file_to_index(self.file(tree.children[0]))
        elif child_index_is_type(tree, 0, "rank"):
            required_rank = int(self.rank(tree.children[0])) - 1
        return required_file, required_rank

    def promotion(self, tree):
        promotion = tree.children[1].children[0].data
        promotion = promotion.upper() if self.board.current_player == 1 else promotion
        self.promotion_type = promotion

    def castle(self, tree):
        piece = self.set_piece("k")
        if tree.data == "king_side_castle":
            to_coord = (6, 0) if self.board.current_player == WHITE else (6, 7)
        elif tree.data == "queen_side_castle":
            to_coord = (2, 0) if self.board.current_player == WHITE else (2, 7)
        return piece, to_coord

    def set_piece(self, piece):
        self.piece = str(piece).upper()
