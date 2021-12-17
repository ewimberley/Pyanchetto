from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from ai.priority_heuristic import PriorityHueristic

piece_values = (0, 10, 9, 5, 3, 3, 1, 10, 9, 5, 3, 3, 1)

class PiecePriorityHeuristic(PriorityHueristic):
    def __init__(self):
        super().__init__()

    def compute_heuristic(self, move, board):
        return piece_values[board.get_coord(move[0])]