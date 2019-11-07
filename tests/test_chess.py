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

    def test_get_piece_color(self):
        colors = []
        true_colors = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        for i in range(8):
            for j in range(8):
                colors.append(self.board.get_piece_color(j,i))
        assert colors == true_colors

    def test_valid_pawn_moves(self):
        black_pawn_true_moves = [(0, 2), (0, 3)]
        black_pawn_moves = self.board.pawn_moves(0, 1)
        assert black_pawn_moves == black_pawn_true_moves

    def test_valid_rook_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 3
        moves = self.board.rook_moves(4, 4)
        true_moves = [(4,5),(4,6),(4,7),(4,3),(4,2),(4,1),(4,0),(5,4),(6,4),(7,4),(3,4),(2,4),(1,4),(0,4)]
        assert moves == true_moves

    def test_valid_bishop_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 4
        true_moves = [(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3), (6, 2), (7, 1)]
        moves = self.board.bishop_moves(4, 4)
        assert moves == true_moves

    def test_valid_queen_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 2
        true_moves = [(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3), (6, 2), (7, 1), (4, 5), (4, 6), (4, 7), (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4)]
        moves = self.board.queen_moves(4, 4)
        assert moves == true_moves

    def test_valid_king_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 1
        true_moves = [(5, 5), (3, 3), (5, 3), (3, 5), (4, 5), (4, 3), (5, 4), (3, 4)]
        moves = self.board.king_moves(4, 4)
        assert moves == true_moves

    def test_valid_moves(self):
        moves = self.board.valid_moves()
        assert 20 == len(moves)
