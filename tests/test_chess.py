import unittest

from pyanchetto.chess import *

class TestChess(unittest.TestCase):
    def setUp(self):
        self.board = Chess()

    def tearDown(self):
        pass

    def test_init(self):
        assert self.board.fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def test_get_piece_color(self):
        colors = []
        true_colors = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2,2]
        for i in range(8):
            for j in range(8):
                colors.append(self.board.color((j, i)))
        assert colors == true_colors

    def test_valid_pawn_moves(self):
        black_pawn_true_moves = [(0, 2, False), (0, 3, False)]
        black_pawn_moves = list(self.board.pawn(0, 1))
        assert black_pawn_moves == black_pawn_true_moves

    def test_valid_promotion_moves(self):
        self.board.board = self.empty_board()
        self.board.board[6][4] = 6
        white_pawn_true_moves = [(4, 7, False, 'Q'), (4, 7, False, 'R'), (4, 7, False, 'B'), (4, 7, False, 'N')] 
        white_pawn_moves = list(self.board.pawn(4, 6))
        assert white_pawn_moves == white_pawn_true_moves

    def test_valid_rook_moves(self):
        self.board.board = self.empty_board()
        self.board.board[4][4] = 3
        true_moves = [(4, 5, True), (4, 6, True), (4, 7, True), (4, 3, True), (4, 2, True), (4, 1, True), (4, 0, True),
                      (5, 4, True), (6, 4, True), (7, 4, True), (3, 4, True), (2, 4, True), (1, 4, True), (0, 4, True)]
        moves = list(self.board.rook(4, 4))
        assert moves == true_moves

    def test_valid_bishop_moves(self):
        self.board.board = self.empty_board()
        self.board.board[4][4] = 4
        true_moves = [(5, 5, True), (6, 6, True), (7, 7, True), (3, 3, True), (2, 2, True), (1, 1, True),
                      (0, 0, True), (3, 5, True), (2, 6, True), (1, 7, True), (5, 3, True), (6, 2, True), (7, 1, True)]
        moves = list(self.board.bishop(4, 4))
        assert moves == true_moves

    #TODO test knight moves

    def test_valid_queen_moves(self):
        self.board.board = self.empty_board()
        self.board.board[4][4] = 2
        true_moves = [(5, 5, True), (6, 6, True), (7, 7, True), (3, 3, True), (2, 2, True), (1, 1, True), (0, 0, True),
                      (3, 5, True), (2, 6, True), (1, 7, True), (5, 3, True), (6, 2, True), (7, 1, True), (4, 5, True),
                      (4, 6, True), (4, 7, True), (4, 3, True), (4, 2, True), (4, 1, True), (4, 0, True), (5, 4, True),
                      (6, 4, True), (7, 4, True), (3, 4, True), (2, 4, True), (1, 4, True), (0, 4, True)]
        moves = list(self.board.queen(4, 4))
        assert moves == true_moves

    def test_valid_king_moves(self):
        self.board.board = self.empty_board()
        self.board.board[4][4] = 1
        self.board.kings_moved[0] = True
        true_moves = [(5, 5, True), (3, 3, True), (5, 3, True), (3, 5, True), (4, 5, True), (4, 3, True),
                      (5, 4, True), (3, 4, True)]
        moves = list(self.board.king(4, 4))
        assert moves == true_moves

    def test_valid_king_moves_castle(self):
        self.board.board = self.empty_board()
        self.board.board[0][4] = 1
        self.board.board[0][0] = 3
        self.board.board[0][7] = 3
        self.board.board[7][4] = 7
        self.board.board[7][0] = 9
        self.board.board[7][7] = 9
        self.board.init_player_pieces()
        true_moves = [(2, 0, False), (6, 0, False), (5, 1, True), (3, 1, True), (4, 1, True), (5, 0, True), (3, 0, True)]
        moves = list(self.board.king(4, 0))
        assert moves == true_moves
        true_moves = [(2, 7, False), (6, 7, False), (3, 6, True), (5, 6, True), (4, 6, True), (5, 7, True), (3, 7, True)]
        moves = list(self.board.king(4, 7))
        assert moves == true_moves
        self.board.move((4, 0), (2, 0, False))
        assert self.board.fen() == "r3k2r/8/8/8/8/8/8/2KR3R b kq - 1 1"
        self.board.move((4, 7), (6, 7, False))
        #print(self.board.fen())
        assert self.board.fen() == "r4rk1/8/8/8/8/8/8/2KR3R w - - 2 2"

    def test_valid_opening_moves(self):
        moves = self.board.valid_moves()
        assert 16 == len(moves)
        to_coords = []
        for piece in moves:
            to_coords.extend(moves[piece])
        assert 20 == len(to_coords)

    def test_check_check(self):
        self.board.board = self.empty_board()
        self.board.board[4][4] = 1
        self.board.init_player_pieces()
        assert not self.board.check_check(self.board.current_player)
        self.board.board[2][4] = 8
        self.board.init_player_pieces()
        assert self.board.check_check(self.board.current_player)
        #TODO check that non-threatening moves do not place king in check

    def test_captured(self):
        self.board.board = self.empty_board()
        self.board.captured_pieces[0] = (6, (4,4))
        self.board.move_list.append(((0,0), (4,4)))
        self.assertListEqual([6], self.board.get_captured_pieces())

    def test_pgn(self):
        self.board.move((0, 1), (0, 2, False))
        pgn = self.board.pgn()
        self.assertEqual("1. a3", pgn)

    def test_board_state(self):
        self.assertEqual(NORMAL, self.board.game_state())
        self.board.move((1, 0), (2, 2, True))
        self.board.move((5, 6), (5, 4, False))
        self.board.move((4, 1), (4, 3, False))
        self.board.move((5, 4), (4, 3, True))
        self.board.move((2, 2), (4, 3, True))
        self.board.move((6, 7), (5, 5, True))
        self.board.move((4, 3), (5, 5, True))
        self.board.move((6, 6), (5, 5, True))
        self.board.move((3, 0), (7, 4, True))
        self.assertEqual(CHECKMATE, self.board.game_state())

    def empty_board(self):
        return [[0 for col in range(8)] for row in range(8)]
