from pyanchetto.chess import NORMAL, CHECK, CHECKMATE, STALEMATE

class MoveTree(object):

    def __init__(self, move):
        self.move = move
        self.children = []
        self.heuristic = 0.0
        self.board = None
        self.capture = False
        self.en_pessant = False
        self.castle = False
        self.promotion = False
        self.game_state = NORMAL

    def add_moves(self, moves_dict):
        for piece in moves_dict:
            for move in moves_dict[piece]:
                self.children.append(MoveTree((piece, move)))

    def prettyPrint(self, depth = 0):
        tree_str = "  " * depth
        tree_str += str(self.move) + "\n"
        for child in self.children:
            tree_str += child.prettyPrint(depth + 1)
        return tree_str

    def count_nodes(self, root=True):
        count = len(self.children)
        count += 1 if root else 0
        for child in self.children:
            count += child.count_nodes(False)
        return count

    def count_nodes_at_depth(self, depth, at_depth = 0):
        if at_depth > depth:
            return 0
        count = len(self.children)
        for child in self.children:
            count += child.count_nodes_at_depth(depth, at_depth + 1)
        return count
