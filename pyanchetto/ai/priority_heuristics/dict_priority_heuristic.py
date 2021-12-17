from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from ai.priority_heuristic import PriorityHueristic


class DictPriorityHeuristic(PriorityHueristic):
    def __init__(self, move_dict):
        super().__init__()
        self.move_dict = move_dict

    def compute_heuristic(self, move, board):
        clone = Chess(board)
        clone.move(move[0], move[1], pgn_gen=False, validate=False, notify=False)
        short_fen = clone.collapsed_fen()
        if short_fen in self.move_dict:
            return 10.0
        return 0.0
