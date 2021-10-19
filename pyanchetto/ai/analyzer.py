import traceback

from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from pyanchetto.move_tree import *
from ai.material_heuristic import MaterialHeuristic

class ChessAnalyzer:
    
    def __init__(self, board, heuristic):
        self.tree = MoveTree("Root")
        self.current_node = self.tree
        self.tree.board = board
        self.heuristic = heuristic

    def analyze(self, node=None, levels=1, player=None):
        if node is None:
            node = self.current_node
        board = node.board
        if player is None:
            player = board.current_player
        moves, player = self.get_moves(board, player)
        for move in moves:
            clone = Chess(board)
            clone.move(move[0], move[1], pgn_gen=False, validate=False, notify=False)
            heuristic = self.heuristic.compute_heuristic(clone, player)
            child = MoveTree(move, parent=node, board=clone, heuristic=heuristic)
            node.children.append(child)
            if levels == 1:
                self.update_best_child(board, child, heuristic, player, node)
            else:
                self.analyze(child, levels-1, player)
        if len(node.children) == 0:
            node.best_child_result = node.heuristic
        if levels > 1:
            for child in node.children:
                try:
                    self.update_best_child(board, child, child.best_child_result, player, node)
                except Exception as e:
                    print(traceback.format_exc())

    def update_best_child(self, board, child, child_heuristic, player, node):
        if node.best_child is None:
            node.best_child = child
            node.best_child_result = child_heuristic
        if board.current_player == player:
            if child_heuristic > node.best_child_result:
                node.best_child = child
                node.best_child_result = child_heuristic
        else:
            if child_heuristic < node.best_child_result:
                node.best_child = child
                node.best_child_result = child_heuristic

    def get_moves(self, board, player):
        piece_moves = board.valid_moves()
        moves = []
        for piece in piece_moves:
            for move in piece_moves[piece]:
                moves.append((piece, move))
        return moves, player

    def apply_move(self, move):
        for child in self.current_node.children:
            if child.move == move:
                self.current_node = child
        #FIXME error if invalid move

if __name__ == '__main__':
    board = Chess()
    analyzer = ChessAnalyzer(board, MaterialHeuristic())
    analyzer.analyze(levels=4)
    print(analyzer.tree.prettyPrint(best_only=True, print_board=True))
    print("")