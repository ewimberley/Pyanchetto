import unittest
import numpy as np

from chess import Chess
from chess_parser import parse_notation
from pgn_interpreter import ChessInterpreter


class TestCube(unittest.TestCase):
    def setUp(self):
        self.board = Chess()
        self.interpreter = ChessInterpreter(self.board)

    def tearDown(self):
        pass

    def test_game(self):
        game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
        tree = parse_notation(game)
        #print(tree.pretty())
        self.interpreter.execute(tree)

