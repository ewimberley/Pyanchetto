from player import Player
from chess import *
from .analyzer import *

class AIPlayer(Player):
    def __init__(self, color, heuristic):
        super().__init__(color)
        self.heuristic = heuristic

    def set_board(self, board):
        super().set_board(board)

    def get_move(self):
        if self.board.current_player != self.color:
            return None, None
        analyzer = ChessAnalyzer(self.board, self.heuristic)
        analyzer.analyze(levels=4)
        best_node = analyzer.current_node.best_child
        if best_node is None:
            print("")
        return best_node.move


    def notify_move(self, move):
        pass
