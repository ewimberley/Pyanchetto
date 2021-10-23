import math
import traceback

from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from pyanchetto.move_tree import *
from pyanchetto.ai.material_heuristic import MaterialHeuristic, piece_values

class ChessAnalyzer:
    
    def __init__(self, board, heuristic):
        self.tree = MoveTree("Root")
        self.current_node = self.tree
        self.tree.board = board
        self.heuristic = heuristic
        self.fen_set = set()
        self.pruned = []
        self.nodes_searched = 0

    def analyze(self, node=None, levels=1, player=None, parent_heuristic=None):
        if node is None:
            node = self.current_node
        board = node.board
        if player is None:
            player = board.current_player
        if parent_heuristic is None:
            parent_heuristic = self.heuristic.compute_heuristic(board, player)
        #return self.analyze_bfs(node, levels, player, parent_heuristic)
        return self.analyze_alpha_beta(node, levels, player, parent_heuristic)

    def analyze_alpha_beta(self, node=None, levels=1, player=None, a=-math.inf, b=math.inf, parent_heuristic=None):
        board = node.board
        moves = self.get_moves(board)
        for move in moves:
            clone = Chess(board)
            clone.move(move[0], move[1], pgn_gen=False, validate=False, notify=False)
            heuristic = self.heuristic.compute_heuristic(clone, player)
            child = MoveTree(move, parent=node, board=clone, heuristic=heuristic)
            node.children.append(child)
            if levels == 1:
                self.update_best_child(board, child, heuristic, player, node)
            else:
                # don't search cycles
                fen = clone.fen()
                if fen in self.fen_set:
                    continue
                self.fen_set.add(fen)
                best = self.analyze_alpha_beta(child, levels-1, player, heuristic)
                if board.current_player == player:
                    a = max(best, a)
                else:
                    b = min(best, b)
                if b <= a:
                    self.pruned.append((node, len(moves)-len(node.children)))
                    break
        if len(node.children) == 0:
            node.best_child_result = node.heuristic
        if levels > 1:
            for child in node.children:
                try:
                    child_heuristic = child.best_child_result if child.best_child_result else child.heuristic
                    self.update_best_child(board, child, child_heuristic, player, node)
                except Exception as e:
                    print(traceback.format_exc())
        self.nodes_searched += len(node.children)
        return node.best_child_result


    def analyze_bfs(self, node=None, levels=1, player=None, parent_heuristic=None):
        board = node.board
        moves = self.get_moves(board)
        for move in moves:
            clone = Chess(board)
            clone.move(move[0], move[1], pgn_gen=False, validate=False, notify=False)
            self.nodes_searched += 1
            heuristic = self.heuristic.compute_heuristic(clone, player)
            heuristic_delta = heuristic - parent_heuristic
            child = MoveTree(move, parent=node, board=clone, heuristic=heuristic)
            node.children.append(child)
            if levels == 1:
                self.update_best_child(board, child, heuristic, player, node)
                if heuristic_delta >= 3:
                    self.analyze_bfs(child, 1, player, heuristic)
            else:
                # don't search cycles
                fen = clone.fen()
                if fen in self.fen_set:
                    continue
                self.fen_set.add(fen)

                levels_remaining = levels - 1
                if heuristic_delta >= 3:
                    levels_remaining = levels
                self.analyze_bfs(child, levels_remaining, player, heuristic)
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

    def get_moves(self, board):
        piece_moves = board.valid_moves()
        moves = []
        for piece in piece_moves:
            for move in piece_moves[piece]:
                moves.append((piece, move))
        def sort_key(x):
            return piece_values[board.get_coord(x[0])]
        moves.sort(reverse=True, key=sort_key)
        return moves

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