from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from ai.priority_heuristic import PriorityHueristic

class EnsemblePriorityHeuristic(PriorityHueristic):
    def __init__(self, heuristics, weights):
        super().__init__()
        self.heuristics = heuristics
        self.weights = weights

    def compute_heuristic(self, move, board):
        scores = []
        for i in range(len(self.heuristics)):
            heuristic = self.heuristics[i]
            weight = self.weights[i]
            scores.append(heuristic.compute_heuristic(move, board)*weight)
        return sum(scores)