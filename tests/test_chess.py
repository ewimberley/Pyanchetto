import unittest

import numpy as np
from chess import Chess


class TestChess(unittest.TestCase):
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
                colors.append(self.board.color((j, i)))
        assert colors == true_colors

    def test_valid_pawn_moves(self):
        black_pawn_true_moves = [(0, 2), (0, 3)]
        black_pawn_moves = self.board.pawn(0, 1)
        assert black_pawn_moves == black_pawn_true_moves

    def test_valid_promotion_moves(self):
        self.board.board.fill(0)
        self.board.board[6][4] = 6
        white_pawn_true_moves = [(4, 7, 'Q'), (4, 7, 'R'), (4, 7, 'B'), (4, 7, 'N')]
        white_pawn_moves = self.board.pawn(4, 6)
        assert white_pawn_moves == white_pawn_true_moves

    def test_valid_rook_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 3
        moves = self.board.rook(4, 4)
        true_moves = [(4,5),(4,6),(4,7),(4,3),(4,2),(4,1),(4,0),(5,4),(6,4),(7,4),(3,4),(2,4),(1,4),(0,4)]
        assert moves == true_moves

    def test_valid_bishop_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 4
        true_moves = [(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3), (6, 2), (7, 1)]
        moves = self.board.bishop(4, 4)
        assert moves == true_moves

    #TODO test knight moves

    def test_valid_queen_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 2
        true_moves = [(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3), (6, 2), (7, 1), (4, 5), (4, 6), (4, 7), (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4)]
        moves = self.board.queen(4, 4)
        assert moves == true_moves

    def test_valid_king_moves(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 1
        self.board.kings_moved[0] = True
        true_moves = [(5, 5), (3, 3), (5, 3), (3, 5), (4, 5), (4, 3), (5, 4), (3, 4)]
        moves = self.board.king(4, 4)
        assert moves == true_moves

    def test_valid_king_moves_castle(self):
        self.board.board.fill(0)
        self.board.board[0][4] = 1
        self.board.board[0][0] = 3
        self.board.board[0][7] = 3
        self.board.board[7][4] = 7
        self.board.board[7][0] = 9
        self.board.board[7][7] = 9
        true_moves = [(2, 0), (6, 0), (5, 1), (3, 1), (4, 1), (5, 0), (3, 0)]
        moves = self.board.king(4, 0)
        assert moves == true_moves
        true_moves = [(2, 7), (6, 7), (3, 6), (5, 6), (4, 6), (5, 7), (3, 7)]
        moves = self.board.king(4, 7)
        assert moves == true_moves
        self.board.move((4, 0), (2, 0))
        assert self.board.hash() == "r...k..r..................................................KR...R"
        self.board.move((4, 7), (6, 7))
        assert self.board.hash() == "r....rk...................................................KR...R"

    def test_valid_opening_moves(self):
        moves = self.board.valid_moves()
        assert 20 == len(moves)

    def test_check_check(self):
        self.board.board.fill(0)
        self.board.board[4][4] = 7
        assert not self.board.check_check(self.board.valid_moves())
        self.board.board[2][4] = 2
        assert self.board.check_check(self.board.valid_moves())
