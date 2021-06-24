import unittest

from pyanchetto.pgn_parser import parse_notation

class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse(self, move):
        tree, tokens = parse_notation(move)
        return tree, tokens

    def test_simple(self):
        move = "1. Nc3 Nf6"
        self.parse(move)

    def test_king_side_castle(self):
        move = "1. 0-0"
        tree = self.parse(move)
        #XXX fix this test
        #nodes = tree.find_data("king_side_castle")
        #for node in nodes:
        #    print(node)

    def test_queen_side_castle(self):
        move = "1. 0-0-0"
        self.parse(move)

    def test_second_move_coord_only(self):
        move = "1. Nc3 f5"
        self.parse(move)

    def test_capture(self):
        move = "2. e4 fxe4"
        self.parse(move)

    def test_move_modifiers(self):
        move = "31. Nc3 Nf6#???!!!!!"
        self.parse(move)

    def test_comment(self):
        move = "1. Nc3 {test1} f5 { test2 } 1/2-1/2"
        self.parse(move)

    def test_non_standard_move_numbers(self):
        move = "1... Nc3 1. f5 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', '.', '.', ' ', 'N', 'c', '3', ' ', '1', '.', ' ', 'f', '5', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],cord: [file: [c],rank: [3]]],move_number: [1],move: [cord: [file: [f],rank: [5]]]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_complete_game(self):
        move = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5# 1-0"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'N', 'c', '3', ' ', 'f', '5', ' ', '2', '.', ' ', 'e', '4', ' ', 'f', 'x', 'e', '4', ' ', '3', '.', ' ', 'N', 'x', 'e', '4', ' ', 'N', 'f', '6', ' ', '4', '.', ' ', 'N', 'x', 'f', '6', '+', ' ', 'g', 'x', 'f', '6', ' ', '5', '.', ' ', 'Q', 'h', '5', '#', ' ', '1', '-', '0']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],cord: [file: [c],rank: [3]]],move: [cord: [file: [f],rank: [5]]]],turn: [move_number: [2],move: [cord: [file: [e],rank: [4]]],move: [file: [f],capture,cord: [file: [e],rank: [4]]]],turn: [move_number: [3],move: [piece_type: [N],capture,cord: [file: [e],rank: [4]]],move: [piece_type: [N],cord: [file: [f],rank: [6]]]],turn: [move_number: [4],move: [piece_type: [N],capture,cord: [file: [f],rank: [6]],move_modifiers: [+]],move: [file: [g],capture,cord: [file: [f],rank: [6]]]],turn: [move_number: [5],move: [piece_type: [Q],cord: [file: [h],rank: [5]],move_modifiers: [#]]],outcome: [white_win]]]"
        assert str(tree) == tree_str
        

