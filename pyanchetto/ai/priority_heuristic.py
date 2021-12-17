from abc import ABC, abstractmethod

class PriorityHueristic(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def compute_heuristic(self, move, board):
        pass