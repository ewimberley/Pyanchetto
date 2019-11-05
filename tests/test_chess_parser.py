import unittest
import numpy as np
from chess_parser import parse_notation

class TestCube(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse(self, move):
        print(move + "\n" + "*"*20)
        tree = parse_notation(move)
        print(tree.pretty())

    def test_simple(self):
        move = "1. Nc3 Nf6"
        self.parse(move)

    def test_second_move_coord_only(self):
        move = "1. Nc3 f5"
        self.parse(move)

    #def test_complex(self):
    #    move = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
    #    self.parse(move)

