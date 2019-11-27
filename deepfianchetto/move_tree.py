
class MoveTree(object):

    def __init__(self, move):
        self.move = move
        self.children = []
        self.heuristic = 0.0
        self.board = None

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

    def count_nodes(self):
        count = len(self.children)
        for child in self.children:
            count += child.count_nodes()
        return count

    def count_nodes_at_depth(self, depth, at_depth = 0):
        if at_depth > depth:
            return 0
        count = len(self.children)
        for child in self.children:
            count += child.count_nodes_at_depth(depth, at_depth + 1)
        return count
