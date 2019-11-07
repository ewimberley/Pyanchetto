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

    def simple_game_test(self, game, correct_hash):
        tree = parse_notation(game)
        #print(tree.pretty())
        self.interpreter.execute(tree, False)
        print(self.board.hash())
        assert self.board.hash() == correct_hash

    def test_game_simplest(self):
        game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
        correct_hash = "rnbqkb.rppppp..p.....p.........Q................PPPP.PPPR.B.KBNR"
        self.simple_game_test(game, correct_hash)

    def test_game_unfinished(self):
        game = "1.d4 d5 2.c4 e6 3.Nf3 c5 4.cxd5 exd5 5.g3 Nc6 6.Bg2 Nf6 7.O-O Be7 8.Nc3 O-O 9.dxc5 Bxc5 10.Na4 Be7 11.Be3 Re8 12.Rc1 Bg4"
        correct_hash = ""
        self.simple_game_test(game, correct_hash)

