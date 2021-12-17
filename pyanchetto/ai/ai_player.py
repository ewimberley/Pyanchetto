from .player import Player
from .analyzer import *

class AIPlayer(Player):
    def __init__(self, color, heuristic, priority_heuristic, move_dict):
        super().__init__(color)
        self.heuristic = heuristic
        self.priority_heuristic = priority_heuristic
        self.move_dict = move_dict

    def set_board(self, board):
        super().set_board(board)

    def get_move(self):
        if self.board.current_player != self.color:
            return None, None
        dict_move, dict_freq = self.dictionary_candidate()
        if dict_freq > 1:
            print(f"Dictionary candidate: {dict_move}: {dict_freq}")
            return dict_move
        analyzer = ChessAnalyzer(self.board, self.heuristic, self.priority_heuristic)
        analyzer.analyze(levels=3)
        best_node = analyzer.current_node.best_child
        if best_node is None:
            print("")
        return best_node.move

    def dictionary_candidate(self):
        short_fen = self.board.collapsed_fen()
        if short_fen in self.move_dict:
            candidates = self.move_dict[short_fen]
            max_candidate = None
            max_candidate_count = 0
            for candidate in candidates:
                if max_candidate is None:
                    max_candidate = candidate
                    max_candidate_count = candidates[candidate]
                if candidates[candidate] > max_candidate_count:
                    max_candidate_fen = candidate
                    max_candidate_count = candidates[candidate]
            if max_candidate:
                return max_candidate, max_candidate_count
        return None, 0

    def notify_move(self, move):
        pass
