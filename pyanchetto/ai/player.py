from abc import ABC, abstractmethod

from pyanchetto.chess import *
from pyanchetto.ai.analyzer import *

class Player(ABC):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def set_board(self, board):
        self.board = board

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def notify_move(self, move):
        pass

