class Token:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"{self.data}"

    def __repr__(self):
        return f"'{self}'"

class Lexer:
    def __init__(self, lexemes, string):
        self.cursor = 0
        self.lexemes = lexemes
        self.string = string

    def set_lexemes(self, lexemes):
        self.lexemes = lexemes

    def lookahead(self, lookahead=1):
        cursor_buffer = self.cursor
        tokens = []
        for i in range(lookahead):
            t = self.parse_next_token()
            if t is not None:
                tokens.append(t)
        self.cursor = cursor_buffer
        return tokens

    def parse_next_token(self):
        while self.cursor < len(self.string):
            t = self.string[self.cursor]
            if t in self.lexemes:
                current = Token(t)
                self.cursor += 1
                return current
            elif t in [" ", "\n", "\r", "\t"]: #ignore non-lexeme whitespace
                self.cursor += 1
            else:
                atom_str = self.atom(self.cursor)
                atom = Token(atom_str)
                self.cursor += len(atom_str)
                return atom

    def atom(self, i):
        #XXX this can cause an infinite loop if it returns an empty string
        j = i
        while j < len(self.string):
            current = self.string[j]
            #if current.isalnum():
            if not current.isspace() and current not in self.lexemes:
                j += 1
            else:
                return self.string[i:j]
            if j == len(self.string):
                return self.string[i:j]