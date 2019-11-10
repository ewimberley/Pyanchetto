import unittest
import numpy as np

from chess import Chess
from chess_parser import parse_notation, parse_file
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
        self.interpreter.execute(tree, True)
        #print(self.board.hash())
        print(self.board)
        assert self.board.hash() == correct_hash

    def test_game_file(self):
        tree = parse_file("../examplepgn/1001718.pgn")
        #print(tree.pretty())
        self.interpreter.execute(tree, True)
        #print(self.board.hash())
        assert self.board.hash() == ""

    def test_game_simplest(self):
        game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
        correct_hash = "rnbqkb.rppppp..p.....p.........Q................PPPP.PPPR.B.KBNR"
        self.simple_game_test(game, correct_hash)

    def test_game_unfinished(self):
        game = """1.d4 d5 2.c4 e6 3.Nf3 c5 4.cxd5 exd5 5.g3 Nc6 6.Bg2 Nf6 7.O-O Be7 
            8.Nc3 O-O 9.dxc5 Bxc5 10.Na4 Be7 11.Be3 Re8 12.Rc1 Bg4"""
        correct_hash = "r..qr.k.pp..bppp..n..n.....p....N.....b.....BNP.PP..PPBP..RQ.RK."
        self.simple_game_test(game, correct_hash)

    def test_game_unfinished2(self):
        game = """1. d4 Nf6 2. c4 e6 3. Nf3 d5 4. Nc3 Bb4 5. Bg5 dxc4 6. e4 c5 7. e5 cxd4 
        8. Nxd4 Bxc3+ 9. bxc3 Qa5 10. exf6 Qxg5 11. fxg7 Qxg7 12. Qd2 O-O 13. Bxc4 Rd8 
        14. Qe3 Bd7 15. O-O-O Nc6 16. Bb3 Be8 17. Nxc6 Bxc6 18. h4 Qf6 19. Rh3 b5 20. Rg3+ Kh8 
        21. Rg4 a5 22. Rf4 Qg7 23. Rxd8+ Rxd8 24. g4 b4 25. g5 bxc3 26. Bc2 Bd5 27. Rf6 Qf8 
        28. Qxc3 Rc8 29. Qd3 Qg7 30. f4 Kg8 31. Kd2 h6 32. a3 hxg5 33. fxg5 Rc4 34. Qg3 Be4 
        35. Bb3 Rd4+ 36. Ke1 Bf5 37. h5 Rd3 38. Qb8+ Qf8 39. Qxf8+ Kxf8 40. Bc2 Rh3 41. Bxf5 exf5 
        42. h6 Kg8 43. a4 Rh4 44. Rxf5 Rxa4 45. Kf2 Rg4 46. Kf3 Rg1 47. Kf2 Rg4 48. Kf3 Rg1 
        49. Kf2""" # 1/2-1/2"
        correct_hash = "......k......p.........Pp....RP......................K........r."
        self.simple_game_test(game, correct_hash)

