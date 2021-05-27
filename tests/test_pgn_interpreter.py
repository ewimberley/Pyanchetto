import unittest
import os

from pyanchetto.chess import Chess, STALEMATE, CHECKMATE, NORMAL
from pyanchetto.chess_parser import parse_notation, parse_file
from pyanchetto.pgn_interpreter import ChessInterpreter


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.board = Chess()
        self.interpreter = ChessInterpreter(self.board)

    def tearDown(self):
        pass

    def simple_game_test(self, pgn, correct_hash):
        tree = parse_notation(pgn)
        #print(tree.pretty())
        self.interpreter.execute(tree, False)
        #print(self.board.fen())
        #print(self.board)
        assert self.board.fen() == correct_hash
        #print(self.board.pgn())
        tree2 = parse_notation(self.board.pgn())
        board2 = Chess()
        interpreter2 = ChessInterpreter(board2)
        interpreter2.execute(tree2, False)
        assert board2.fen() == correct_hash

    def game_file_test(self, file, correct_hash):
        if "examplepgn" in os.listdir("."):
            example_path = "examplepgn/"
        else:
            example_path = "../examplepgn/"
        tree = parse_file(example_path + file)
        #print(tree.pretty())
        #self.interpreter.execute(tree, True)
        self.interpreter.execute(tree, False)
        #print(self.board.fen())
        #print(self.board)
        #print(self.board.pgn())
        assert self.board.fen() == correct_hash
        tree2 = parse_notation(self.board.pgn())
        #print(self.board.pgn())
        board2 = Chess()
        interpreter2 = ChessInterpreter(board2)
        interpreter2.execute(tree2, False)
        assert board2.fen() == correct_hash

    def test_game_file(self):
        self.game_file_test("test_game1.pgn", "8/8/8/7p/5k1P/7K/7P/8 w - - 1 76")

    def test_game_file2(self):
        self.game_file_test("test_game2.pgn", "4r3/7P/6K1/8/8/3k4/8/8 b - - 2 62")

    def test_game_file3(self):
        self.game_file_test("test_game3.pgn", "8/p7/k7/7K/6P1/5P2/8/8 b - - 0 63")

    def test_game_file4(self):
        self.game_file_test("test_game4.pgn", "8/1r6/5R2/4pP2/4P3/1pkP1K2/8/8 w - - 1 62")

    def test_game_file5(self):
        self.game_file_test("test_game5.pgn", "r1b1r1k1/1p3ppp/p4n2/8/P2p4/4PB1P/1PQ2PPb/R2RBKNq w - - 4 22")

    def test_game_file6(self):
        self.game_file_test("test_game6.pgn", "6R1/8/5k2/6pK/7p/3P2rP/8/8 w - - 13 101")

    def test_game_file7(self):
        self.game_file_test("test_game7.pgn", "8/8/2K5/8/P5p1/3R1r1k/5P2/8 w - - 7 53")

    def test_game_file8(self):
        self.game_file_test("test_game8.pgn", "8/8/5k2/5b2/R6K/8/8/6r1 b - - 113 172")

    def test_game_file9(self):
        self.game_file_test("test_game9.pgn", "8/8/3k2p1/P6p/3pp3/P3b3/2K3PP/4R3 b - - 1 37")

    def test_game_file_nag(self):
        self.game_file_test("test_game_numeric_annotation_glyph.pgn", "rnbq3r/pppp2pp/2N1kP2/2n3B1/1b6/3P4/PP2QPPP/RN1K1B1R b - - 4 11")

    def test_game_promotion_and_check(self):
        self.game_file_test("test_promotion_and_check.pgn", "8/6p1/p3k2p/1P6/5KP1/2N5/8/8 b - - 0 51")

    def test_game_inline_comment(self):
        self.game_file_test("test_inline_comment.pgn", "5R2/1p5k/1qnP2p1/p1p4p/1nQ5/6P1/1P5P/6K1 w - - 0 35")

    def test_game_castle(self):
        self.game_file_test("test_castle.pgn", "8/1p2kppp/2r1b3/2p1p3/2P5/1P2B3/P4PPP/2KR4 b - - 0 22")

    def test_game_stalemate(self):
        self.game_file_test("test_stalemate.pgn", "8/8/1K5p/3R2nk/P3B1p1/6P1/8/8 b - - 0 78")
        assert self.board.game_state() == STALEMATE

    def test_game_en_pessant(self):
        self.game_file_test("test_en_pessant.pgn", "8/6r1/1p1p1k2/r2Pppb1/P1P2P1p/1B1K4/6RP/6R1 b - - 0 50")

    def test_game_promotion(self):
        self.game_file_test("test_promotion.pgn", "3r2k1/p2P1p2/2Q3b1/7p/4q3/2P1b3/PP6/K6R w - - 1 36")

    def test_game_checkmate(self):
        pgn = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
        correct_hash = "rnbqkb1r/ppppp2p/5p2/7Q/8/8/PPPP1PPP/R1B1KBNR b KQkq - 1 5"
        self.simple_game_test(pgn, correct_hash)
        assert self.board.game_state() == CHECKMATE

    def test_game_unfinished(self):
        pgn = """1.d4 d5 2.c4 e6 3.Nf3 c5 4.cxd5 exd5 5.g3 Nc6 6.Bg2 Nf6 7.O-O Be7 
            8.Nc3 O-O 9.dxc5 Bxc5 10.Na4 Be7 11.Be3 Re8 12.Rc1 Bg4"""
        correct_hash = "r2qr1k1/pp2bppp/2n2n2/3p4/N5b1/4BNP1/PP2PPBP/2RQ1RK1 w - - 6 13"
        self.simple_game_test(pgn, correct_hash)
        assert self.board.game_state() == NORMAL

    def test_game_unfinished2(self):
        pgn = """1. d4 Nf6 2. c4 e6 3. Nf3 d5 4. Nc3 Bb4 5. Bg5 dxc4 6. e4 c5 7. e5 cxd4 
        8. Nxd4 Bxc3+ 9. bxc3 Qa5 10. exf6 Qxg5 11. fxg7 Qxg7 12. Qd2 O-O 13. Bxc4 Rd8 
        14. Qe3 Bd7 15. O-O-O Nc6 16. Bb3 Be8 17. Nxc6 Bxc6 18. h4 Qf6 19. Rh3 b5 20. Rg3+ Kh8 
        21. Rg4 a5 22. Rf4 Qg7 23. Rxd8+ Rxd8 24. g4 b4 25. g5 bxc3 26. Bc2 Bd5 27. Rf6 Qf8 
        28. Qxc3 Rc8 29. Qd3 Qg7 30. f4 Kg8 31. Kd2 h6 32. a3 hxg5 33. fxg5 Rc4 34. Qg3 Be4 
        35. Bb3 Rd4+ 36. Ke1 Bf5 37. h5 Rd3 38. Qb8+ Qf8 39. Qxf8+ Kxf8 40. Bc2 Rh3 41. Bxf5 exf5 
        42. h6 Kg8 43. a4 Rh4 44. Rxf5 Rxa4 45. Kf2 Rg4 46. Kf3 Rg1 47. Kf2 Rg4 48. Kf3 Rg1 
        49. Kf2""" # 1/2-1/2"
        correct_hash = "6k1/5p2/7P/p4RP1/8/8/5K2/6r1 b - - 9 49"
        self.simple_game_test(pgn, correct_hash)
        assert self.board.game_state() == NORMAL


    def test_game_ambiguous(self):
        pgn = "1. Nc3 Nf6  2. Nf3 Nc6  3. Nh4 Nb4  4. Nf5 Rg8  5. Ne3 Rh8  6. Ned5"
        correct_hash = "r1bqkb1r/pppppppp/5n2/3N4/1n6/2N5/PPPPPPPP/R1BQKB1R b KQk - 11 6"
        self.simple_game_test(pgn, correct_hash)
        assert self.board.game_state() == NORMAL
