from abc import ABC, abstractmethod

from pyanchetto.chess import *

class Hueristic(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def compute_heuristic(self, board: Chess, player):
        pass