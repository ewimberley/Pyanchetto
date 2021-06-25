import unittest

from pyanchetto.pgn_parser import parse_notation

class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse(self, move):
        parser = parse_notation(move)
        tree = parser.tree
        tokens = parser.tokens
        #parser.pretty_print()
        print(tree)
        print(tokens)
        return tree, tokens

    #def test_simple(self):
    #    move = "1. Nc3 Nf6"
    #    self.parse(move)

    def test_king_side_castle(self):
        move = "1. O-O 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'O', '-', 'O', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [king_side_castle]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_queen_side_castle(self):
        move = "1. O-O-O 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'O', '-', 'O', '-', 'O', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [queen_side_castle]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_move_modifiers(self):
        move = "1. Nc3 Nf6#???!!!!! 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'N', 'c', '3', ' ', 'N', 'f', '6', '#', '?', '?', '?', '!', '!', '!', '!', '!', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],coord: [file: [c],rank: [3]]],move: [piece_type: [N],coord: [file: [f],rank: [6]],move_modifiers: [#,?,?,?,!,!,!,!,!]]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_metadata(self):
        move = "[key value text] 1. Nc3 f5 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['[', 'key', ' ', 'value', ' ', 'text', ']', ' ', '1', '.', ' ', 'N', 'c', '3', ' ', 'f', '5', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [metadata: [key,value text],turn: [move_number: [1],move: [piece_type: [N],coord: [file: [c],rank: [3]]],move: [coord: [file: [f],rank: [5]]]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_comment(self):
        move = "1. Nc3 {test1} f5 { test2 } 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'N', 'c', '3', ' ', '{', 'test1', '}', ' ', 'f', '5', ' ', '{', ' ', 'test2', ' ', '}', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],coord: [file: [c],rank: [3]]],comment: [test1],move: [coord: [file: [f],rank: [5]]],comment: [ test2 ]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_non_standard_move_numbers(self):
        move = "1... Nc3 1. f5 1/2-1/2"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', '.', '.', ' ', 'N', 'c', '3', ' ', '1', '.', ' ', 'f', '5', ' ', '1', '/', '2', '-', '1', '/', '2']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],coord: [file: [c],rank: [3]]],move_number: [1],move: [coord: [file: [f],rank: [5]]]],outcome: [draw]]]"
        assert str(tree) == tree_str

    def test_complete_game(self):
        move = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5# 1-0"
        tree, tokens = self.parse(move)
        tokens_str = "['1', '.', ' ', 'N', 'c', '3', ' ', 'f', '5', ' ', '2', '.', ' ', 'e', '4', ' ', 'f', 'x', 'e', '4', ' ', '3', '.', ' ', 'N', 'x', 'e', '4', ' ', 'N', 'f', '6', ' ', '4', '.', ' ', 'N', 'x', 'f', '6', '+', ' ', 'g', 'x', 'f', '6', ' ', '5', '.', ' ', 'Q', 'h', '5', '#', ' ', '1', '-', '0']"
        assert str(tokens) == tokens_str
        tree_str = "root: [pgn: [turn: [move_number: [1],move: [piece_type: [N],coord: [file: [c],rank: [3]]],move: [coord: [file: [f],rank: [5]]]],turn: [move_number: [2],move: [coord: [file: [e],rank: [4]]],move: [file: [f],capture,coord: [file: [e],rank: [4]]]],turn: [move_number: [3],move: [piece_type: [N],capture,coord: [file: [e],rank: [4]]],move: [piece_type: [N],coord: [file: [f],rank: [6]]]],turn: [move_number: [4],move: [piece_type: [N],capture,coord: [file: [f],rank: [6]],move_modifiers: [+]],move: [file: [g],capture,coord: [file: [f],rank: [6]]]],turn: [move_number: [5],move: [piece_type: [Q],coord: [file: [h],rank: [5]],move_modifiers: [#]]],outcome: [white_win]]]"
        assert str(tree) == tree_str
        

