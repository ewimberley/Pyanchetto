from chess import NORMAL, CHECK, CHECKMATE, STALEMATE

class MoveTree(object):

    def __init__(self, move, board=None, heuristic=0.0, parent=None, en_pessant=False, castle=False, promotion=False):
        self.move = move
        self.parent = parent
        self.children = []
        self.best_child = None
        self.best_child_result = None
        self.heuristic = heuristic
        self.board = board
        self.capture = False
        self.en_pessant = en_pessant
        self.castle = castle
        self.promotion = promotion
        self.game_state = NORMAL

    def add_moves(self, moves_dict):
        for piece in moves_dict:
            for move in moves_dict[piece]:
                self.children.append(MoveTree((piece, move)))

    def prettyPrint(self, depth=0, best=False, best_only=False, print_board=False):
        tree_str = " - " * depth
        if best:
            tree_str += "*"
        tree_str += f"{self.move=}\t{self.heuristic=}\t{self.best_child_result=}\t{self.capture=}\t{self.castle=}\n"
        if print_board:
            tree_str += str(self.board)
        for child in self.children:
            best = child == self.best_child
            if not best_only or (best_only and best):
                tree_str += child.prettyPrint(depth + 1, best, best_only, print_board)
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
