import unittest

import numpy as np
from chess import Chess


class TestCube(unittest.TestCase):
    def setUp(self):
        self.board = Chess()

    def tearDown(self):
        pass

    def test_init(self):
        assert self.board.hash() == "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR"

    def test_parse_algebra(self):
        moves = "F F B B U U D D L L R R"
        #self.cube.parse_moves(moves)
        ##print(self.cube.hash())
        #assert self.cube.hash() == "OROROROROGBGBGBGBGWYWYWYWYWBGBGBGBGBYWYWYWYWYROROROROR"
        #moves = "F' F' B' B' U' U' D' D' L' L' R' R'"
        #self.cube.parse_moves(moves)
        #assert self.cube.hash() == SOLVED_HASH
