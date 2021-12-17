from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from ai.heuristic import Hueristic

class EnsembleHeuristic(Hueristic):
    def __init__(self, heuristics, weights):
        super().__init__()
        self.heuristics = heuristics
        self.weights = weights

    def compute_heuristic(self, board, player):
        scores = []
        for i in range(len(self.heuristics)):
            heuristic = self.heuristics[i]
            weight = self.weights[i]
            scores.append(heuristic.compute_heuristic(board, player)*weight)
        return sum(scores)