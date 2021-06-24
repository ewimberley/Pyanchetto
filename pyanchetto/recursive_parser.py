from functools import wraps
import re

class Lexer:
    def __init__(self, lexemes, string):
        self.lexemes = lexemes
        self.string = string
        self.tokens = []

    def lex(self):
        i = 0
        while i < len(self.string):
            t = self.string[i]
            if t in self.lexemes:
                current = Token(t)
                self.tokens.append(current)
                i += 1
            else:
                atom_str = self.atom(i)
                atom = Token(atom_str)
                self.tokens.append(atom)
                i += len(atom_str)

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


class Token:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"{self.data}"

    def __repr__(self):
        return f"'{self}'"

class SyntaxError(Exception):
    def __init__(self, description, token, token_num, token_stream):
        end = min(token_num+10, len(token_stream))
        str_at_token = "".join([str(t) for t in token_stream[token_num:end]])
        self.message = f"Expected {description}, found token '{token}' instead. Error near: '{str_at_token}'"
        super().__init__(self.message)

def ast(data):
    def _ast(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            self.create_push(data)
            func(self, *args, **kwargs)
            self.ast_path.pop()
        return inner
    return _ast

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.on_token = 0
        self.ast_path = []
        self.tree = None

    def pretty_print(self, node=None, level=0):
        if node is None:
            node = self.tree
        indent = "--" * level
        if isinstance(node, Tree):
            print(f"{indent}{node.data}")
            for child in node.children:
                self.pretty_print(child, level+1)
        else:
            print(f"{indent}{node}")


    def parse(self):
        root = Tree("root")
        self.ast_path.append(root)
        self.tree = root
        return True

    def create_push(self, data):
        node = Tree(data)
        self.ast_path[-1].children.append(node)
        self.ast_path.append(node)
        return node

    def create_append(self, data):
        node = Tree(data)
        self.ast_path[-1].children.append(node)
        return node

    def has_next(self):
        return self.on_token < len(self.tokens)

    def consume(self):
        if self.has_next():
            t = self.tokens[self.on_token]
            self.on_token += 1
            return t
        else:
            raise SyntaxError("Unexpected end of token stream.")

    def peak(self):
        if self.has_next():
            return self.tokens[self.on_token]
        else:
           raise SyntaxError("Unexpected end of token stream.")

    def match_pattern(self, pattern):
        for i in range(len(pattern)):
            if (self.on_token + i) >= len(self.tokens):
                return False
            p = pattern[i]
            t  = self.tokens[self.on_token + i]
            if isinstance(p, str):
                if str(t) != p:
                    return False
            elif isinstance(p, list) or isinstance(p, dict) or isinstance(p, set):
                if str(t) not in p:
                    return False
            elif isinstance(p, RegularExpression):
                #forward_string = "".join([str(t) for t in self.tokens[self.on_token:]])
                #if not re.match(p.pattern, forward_string):
                if not re.match(p.pattern, str(t)):
                    return False
        return True

    def accept(self, sym):
        t = self.peak()
        if isinstance(sym, list) or isinstance(sym, dict) or isinstance(sym, set):
            if str(t) in sym:
                self.consume()
                return t
            return False
        else:
            if str(t) == sym:
                self.consume()
                return t
        return False

    def expect(self, sym, description):
        t = self.peak()
        if isinstance(sym, list) or isinstance(sym, dict) or isinstance(sym, set):
            if str(t) not in sym:
                raise SyntaxError(description, t, self.on_token, self.tokens)
        elif str(t) != sym:
            raise SyntaxError(description, t, self.on_token, self.tokens)
        return t

    def consume_whitespace(self):
        if self.has_next():
            while self.accept(' '):
                pass

class RegularExpression:
    def __init__(self, re):
        self.pattern = re

class Tree:
    def __init__(self, data):
        self.data = data
        self.children = []

    def __str__(self):
        if len(self.children) > 0:
            child_str = ",".join([str(child) for child in self.children])
            return f"{self.data}: [{child_str}]"
        return f"{self.data}"

    def __repr__(self):
        return f"'{self}'"
