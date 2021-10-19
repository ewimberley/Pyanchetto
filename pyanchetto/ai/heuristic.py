from abc import ABC, abstractmethod

class Hueristic(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def compute_heuristic(self, board, player):
        pass