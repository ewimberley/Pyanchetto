from yarp_parser.recursive_parser import *

NUMBER_REGEX = "^[0-9]+$"
RANKS = {'1', '2', '3', '4', '5', '6', '7', '8'}
FILES = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
PIECES = {'K', 'Q', 'R', 'B', 'N', 'P'}
CAPTURE = 'x'
PROMOTION = '='
CHECK = '+'
CHECKMATE = '#'
DOT = '.'
GLYPH = '$'
DRAW = ['1', '/', '2', '-', '1', '/', '2']
BLACK_WIN = ['0', '-', '1']
WHITE_WIN = ['1', '-', '0']
KINGSIDE_CASTLE = ['O', '-', 'O']
QUEENSIDE_CASTLE = ['O', '-', 'O', '-', 'O']

normal_mode_lexemes = set({
        #metadata
        '[', ']', '"',
        #comments
        '{', '}',
        #moves
        DOT, PROMOTION, CHECK, CHECKMATE, CAPTURE,
        #quality, annotation
        '?', '!', GLYPH,
        #misc
        '-', '/', ' '
})
normal_mode_lexemes.update(FILES)
normal_mode_lexemes.update(PIECES)


def parse_file(file_name):
    with open(file_name, "r") as file:
        data = file.read()
        return parse_notation(data)


def parse_notation(string):
    parser = PGNParser(string)
    parser.parse()
    return parser


class PGNParser(Parser):

    def parse(self):
        super().parse()
        self.lexer.ignore_whitespace = False
        self.pgn()

    @lexemes(normal_mode_lexemes)
    @ast("pgn")
    def pgn(self):
        self.consume_whitespace()
        #XXX put a max limit on how long this loop can go
        while self.has_next():
            if(self.metadata()):
                pass
            elif self.match_pattern([RegularExpression(NUMBER_REGEX), DOT]):
                self.turn()
            else:
                self.outcome()
            self.consume_whitespace()

    @lexemes({'[', ']', ' '})
    @ast("metadata", optional=['['])
    def metadata(self, tokens):
        key = self.consume()
        self.consume_whitespace()
        value_str = ""
        t = self.consume()
        while str(t) != ']':
            value_str += str(t)
            t = self.consume()
        self.create_append(str(key))
        self.create_append(value_str)
        self.consume_whitespace()
        return True

    @lexemes({'{', '}', ' '})
    @ast("comment", optional=['{'])
    def comment(self, tokens):
        comment_str = ""
        t = self.consume()
        while str(t) != '}':
            comment_str += str(t)
            t = self.consume()
        self.create_append(comment_str)

    @ast("anno_glyph", optional=[GLYPH])
    def anno_glyph(self, tokens):
        num_str = self.parser_number()
        self.create_append(num_str)

    turn_lexemes = normal_mode_lexemes.union({' '})
    @lexemes(turn_lexemes)
    @ast("turn")
    def turn(self):
        space_between_moves = False
        self.move_number()
        self.consume_whitespace()
        self.move()
        space_between_moves = self.consume_whitespace() or space_between_moves
        self.anno_glyph()
        space_between_moves = self.consume_whitespace() or space_between_moves
        self.comment()
        space_between_moves = self.consume_whitespace() or space_between_moves
        if self.match_pattern([RegularExpression(NUMBER_REGEX), DOT]):
            self.move_number()
        space_between_moves = self.consume_whitespace() or space_between_moves
        move_lookahead = PIECES.union(FILES)
        move_lookahead.add('O') #castle
        if self.match_pattern([move_lookahead]):
            if not space_between_moves:
                raise SyntaxError("space between half moves", None, self.lexer)
            self.move()
        self.consume_whitespace()
        self.anno_glyph()
        self.comment()

    @ast("move_number")
    def move_number(self):
        num_str = self.parser_number()
        if num_str == "":
            raise SyntaxError("move number", None, self.lexer)
        self.create_append(num_str)
        t = self.peak()
        while self.accept(DOT):
            pass

    def parser_number(self):
        num_str = ""
        while self.match_pattern([RegularExpression(NUMBER_REGEX)]):
            t = self.consume()
            num_str += str(t)
        return num_str

    @ast("move")
    def move(self):
        self.parse_alternatives([([PIECES], self.simple_move),
                                 ([FILES, CAPTURE, FILES, RANKS], self.ambiguous_rank_move),
                                 ([FILES], self.coord_move),
                                 (QUEENSIDE_CASTLE, self.queen_side_castle),
                                 (KINGSIDE_CASTLE, self.king_side_castle)],
                                "move description")
        if self.match_pattern([[CHECK, CHECKMATE, "!", "?"]]): #FIXME add winning strings?
            self.move_modifiers()

    def simple_move(self): #piece_type disambiguation? capture? coord move_modifiers?
        self.piece_type()
        file_or_rank = FILES.union(RANKS)
        if self.match_pattern([file_or_rank]):
            if self.match_pattern([file_or_rank, CAPTURE, FILES, RANKS]):
                self.disambiguation()
                self.capture()
            elif self.match_pattern([file_or_rank, FILES, RANKS]):
                self.disambiguation()
            self.coord()
        else:
            self.capture()
            self.coord()

    def ambiguous_rank_move(self): #file capture? coord promotion? move_modifiers?
        self.file()
        self.capture()
        self.coord()
        self.promotion()

    def coord_move(self):
        self.coord()
        self.promotion()

    @ast("piece_type", require=[PIECES], description="piece type")
    def piece_type(self, tokens):
        self.create_append(tokens[0])

    @ast("disambiguation")
    def disambiguation(self):
        self.parse_alternatives([([FILES], self.file),
                                 ([RANKS], self.rank)],
                                 "file or rank disambiguation")

    @ast("coord")
    def coord(self):
        self.file()
        self.rank()

    @ast("file", require=[FILES], description="file letter")
    def file(self, tokens):
        self.create_append(str(tokens[0]))

    @ast("rank", require=[RANKS], description="rank number")
    def rank(self, tokens):
        self.create_append(str(tokens[0]))

    @ast("king_side_castle")
    def king_side_castle(self):
        self.consume(3)

    @ast("queen_side_castle")
    def queen_side_castle(self):
        self.consume(5)

    @ast("promotion", optional=[PROMOTION])
    def promotion(self, tokens):
        self.create_append(str(tokens[0]))
        self.piece_type()

    @ast("capture", optional=[CAPTURE])
    def capture(self, tokens):
        pass

    @ast("move_modifiers")
    def move_modifiers(self):
        #TODO refactor this method using parse_alternatives
        #checks
        if self.match_pattern([CHECK]):
            t = self.consume()
            self.create_append(str(t))
        elif self.match_pattern([CHECKMATE]):
            t = self.consume()
            self.create_append(str(t))
        #quality
        t = self.accept(['!', '?'])
        while t:
            self.create_append(str(t))
            t = self.accept(['!', '?'])
        #FIXME winning strgs like +-, +/-, etc

    @ast("outcome")
    def outcome(self):
        self.parse_alternatives([(WHITE_WIN, self.white_win),
                                 (BLACK_WIN, self.black_win),
                                 (DRAW, self.draw)],
                                "winning annotation")

    @ast("white_win", require=WHITE_WIN, description="white winning annotation")
    def white_win(self, tokens):
        pass

    @ast("black_win", require=BLACK_WIN, description="black winning annotation")
    def black_win(self, tokens):
        pass

    @ast("draw", require=DRAW, description="draw annotation")
    def draw(self, tokens):
        pass
