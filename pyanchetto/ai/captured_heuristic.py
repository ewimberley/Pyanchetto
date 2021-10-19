from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from heuristic import Hueristic

piece_values = (0, 100, 9, 5, 3, 3, 1, 100, 9, 5, 3, 3, 1)

class MaterialHeuristic(Hueristic):
    def __init__(self):
        super().__init__()

    def compute_heuristic(self, board, player):
        captured = board.get_captured_pieces()
        score = 0
        for cap in captured:
            if player == 1:
                if cap <= 6:
                    score -= piece_values[cap]
                else:
                    score += piece_values[cap]
            else:
                if cap > 6:
                    score -= piece_values[cap]
                else:
                    score += piece_values[cap]
        return score