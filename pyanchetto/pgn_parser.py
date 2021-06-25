from pyanchetto.recursive_parser import *

RANKS = {'1', '2', '3', '4', '5', '6', '7', '8'}
FILES = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
PIECES = {'K', 'Q', 'R', 'B', 'N', 'P'}
CAPTURE = 'x'
PROMOTION = '='
CHECK = '+'
CHECKMATE = '#'
DOT = '.'
GLYPH = '$'
#WHITE_WIN = "1-0"
#BLACK_WIN = "0-1"
#DRAW = "1/2-1/2"
KINGSIDE_CASTLE = "O-O"
QUEENSIDE_CASTLE = "O-O-O"

normal_mode_lexemes = {
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
}
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
        self.lexer.set_lexemes(normal_mode_lexemes)
        super().parse()
        self.pgn()

    @ast("pgn")
    def pgn(self):
        self.consume_whitespace()
        #XXX put a max limit on how long this loop can go
        while self.has_next():
            t = self.peak()
            if self.match_pattern(['[']):
                self.metadata()
            elif self.match_pattern([RegularExpression("^[0-9]+$"), DOT]):
                self.turn()
            else:
                self.outcome()
            self.consume_whitespace()

    @ast("metadata")
    def metadata(self):
        self.lexer.set_lexemes({'[', ']', ' '})
        t = self.consume()
        key = self.consume()
        value_str = ""
        t = self.consume()
        while str(t) != ']':
            value_str += str(t)
            t = self.consume()
        self.create_append(str(key))
        self.create_append(value_str)
        self.lexer.set_lexemes(normal_mode_lexemes)

    @ast("comment")
    def comment(self):
        self.lexer.set_lexemes({'{', '}', ' '})
        t = self.consume()
        comment_str = ""
        t = self.consume()
        while str(t) != '}':
            comment_str += str(t)
            t = self.consume()
        self.create_append(comment_str)
        self.lexer.set_lexemes(normal_mode_lexemes)

    @ast("anno_glyph")
    def anno_glyph(self):
        t = self.expect(['$'], "annotation glyph ($)")
        self.consume()
        num_str = self.parser_number()
        self.create_append(num_str)

    @ast("turn")
    def turn(self):
        self.move_number()
        self.move()
        self.consume_whitespace()
        if self.match_pattern(['$']):
            self.anno_glyph()
        self.consume_whitespace()
        if self.match_pattern(['{']):
            self.comment()
        self.consume_whitespace()
        if self.match_pattern([RegularExpression("^[0-9]+$"), DOT]):
            self.move_number()
        move_lookahead = PIECES.union(FILES)
        move_lookahead.add('O') #castle
        if self.match_pattern([move_lookahead]):
            self.move()
        self.consume_whitespace()
        if self.match_pattern(['$']):
            self.anno_glyph()
        self.consume_whitespace()
        if self.match_pattern(['{']):
            self.comment()
        self.consume_whitespace()

    @ast("move_number")
    def move_number(self):
        #FIXME expect number here
        num_str = self.parser_number()
        if num_str == "":
            raise SyntaxError("move number", None, self.lexer)
        self.create_append(num_str)
        t = self.peak()
        while self.accept(DOT):
            pass
        self.consume_whitespace()

    def parser_number(self):
        num_str = ""
        while self.match_pattern([RegularExpression("^[0-9]+$")]):
            t = self.consume()
            num_str += str(t)
        return num_str

    @ast("move")
    def move(self):
        if self.match_pattern([PIECES]):
            self.simple_move()
        elif self.match_pattern([FILES]):
            if self.match_pattern([FILES, CAPTURE, FILES, RANKS]) or self.match_pattern([FILES, FILES, RANKS]):
                self.ambiguous_rank_move()
            else:
                self.coord()
            if self.match_pattern([PROMOTION]):
                self.promotion()
        elif self.match_pattern(['O', '-', 'O', '-', 'O']):
            self.queen_side_castle()
        elif self.match_pattern(['O', '-', 'O']):
            self.king_side_castle()
        if self.match_pattern([[CHECK, CHECKMATE, "!", "?"]]): #FIXME add winning strings?
            self.move_modifiers()
        self.consume_whitespace()

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
            if self.match_pattern([CAPTURE]):
                self.capture()
            self.coord()

    def ambiguous_rank_move(self): #file capture? coord promotion? move_modifiers?
        self.file()
        if self.match_pattern([CAPTURE]):
            self.capture()
        self.coord()

    @ast("piece_type")
    def piece_type(self):
        t = self.expect(PIECES, "piece type")
        self.consume()
        self.create_append(t)

    @ast("disambiguation")
    def disambiguation(self):
        if self.match_pattern([FILES]):
            self.file()
        else:
            self.rank()

    @ast("coord")
    def coord(self):
        self.file()
        self.rank()

    @ast("file")
    def file(self):
        t = self.expect({'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}, "file letter")
        self.consume()
        self.create_append(str(t))

    @ast("rank")
    def rank(self):
        t = self.expect(RANKS, "file letter")
        self.consume()
        self.create_append(str(t))

    @ast("king_side_castle")
    def king_side_castle(self):
        self.consume(3)

    @ast("queen_side_castle")
    def queen_side_castle(self):
        self.consume(5)

    @ast("promotion")
    def promotion(self):
        t = self.expect(PROMOTION, 'promotion ("=")')
        self.consume()
        self.create_append(str(t))
        self.piece_type()

    @ast("capture")
    def capture(self):
        self.expect(CAPTURE, 'capture ("x")')
        self.consume()

    @ast("move_modifiers")
    def move_modifiers(self):
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
        if self.match_pattern(['1', '-', '0']):
            self.white_win()
        elif self.match_pattern(['0', '-', '1']):
            self.black_win()
        elif self.match_pattern(['1', '/', '2', '-', '1', '/', '2']):
            self.draw()

    @ast("white_win")
    def white_win(self):
        self.consume(3)

    @ast("black_win")
    def black_win(self):
        self.consume(3)

    @ast("draw")
    def draw(self):
        self.consume(7)
