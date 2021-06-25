from functools import wraps
import re

from pyanchetto.streaming_lexer import *

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

class SyntaxError(Exception):
    def __init__(self, description, token=None, lexer=None):
        end = min(lexer.cursor+20, len(lexer.string))
        str_at_token = "".join([c for c in lexer.string[lexer.cursor:end]])
        if token is not None:
            self.message = f"Expected {description}, found token '{token}' instead. Error near: '{str_at_token}'"
        else:
            self.message = f"Expected {description}. Error near: '{str_at_token}'"
        super().__init__(self.message)


class RegularExpression:
    def __init__(self, re):
        self.pattern = re


def ast(data, require=None, description=None, optional=None):
    def _ast(func):
        def ast_stack_function(self, tokens=None, *args, **kwargs):
            self.create_push(data)
            if tokens is None:
                result = func(self, *args, **kwargs)
            else:
                result = func(self, tokens, *args, **kwargs)
            self.ast_path.pop()
            return result

        @wraps(func)
        def inner(self, *args, **kwargs):
            if require is not None:
                tokens = self.expect_pattern(require, description)
                return ast_stack_function(self, tokens, *args, **kwargs)
            elif optional is not None:
                if self.match_pattern(optional):
                    tokens = [self.accept(f) for f in optional]
                    return ast_stack_function(self, tokens, *args, **kwargs)
            else:
                return ast_stack_function(self, None, *args, **kwargs)
        return inner
    return _ast

def lexemes(lexemes):
    def _lexemes(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            lexemes_buffer = self.lexer.lexemes
            self.lexer.set_lexemes(lexemes)
            result = func(self, *args, **kwargs)
            self.lexer.set_lexemes(lexemes_buffer)
            return result
        return inner
    return _lexemes

class Parser:
    def __init__(self, string):
        self.tokens = []
        self.lexer = Lexer([], string)
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
        self.ast_path.append(self.create_append(data))
        return self.ast_path[-1]

    def create_append(self, data):
        node = Tree(data)
        self.ast_path[-1].children.append(node)
        return node

    def has_next(self):
        return len(self.lexer.lookahead()) == 1

    def consume(self, num_tokens=1):
        if num_tokens > 1:
            return [self.consume() for i in range(num_tokens)]
        elif self.has_next():
            t = self.lexer.parse_next_token()
            self.tokens.append(t)
            return t
        raise SyntaxError("Unexpected end of token stream.")

    def peak(self):
        if self.has_next():
            return self.lexer.lookahead()[0]
        raise SyntaxError("Unexpected end of token stream.")

    def parse_alternatives(self, alternatives, description):
        for alternative in alternatives:
            if self.match_pattern(alternative[0]):
                return alternative[1]()
        raise SyntaxError(description, None, self.lexer)

    def match_pattern(self, pattern):
        lookahead = self.lexer.lookahead(len(pattern))
        if len(lookahead) != len(pattern):
            return False
        for i in range(len(pattern)):
            p = pattern[i]
            t = lookahead[i]
            if isinstance(p, str) and str(t) != p:
                return False
            elif (isinstance(p, list) or isinstance(p, dict) or isinstance(p, set)) and str(t) not in p:
                return False
            elif isinstance(p, RegularExpression) and (not re.match(p.pattern, str(t))):
                return False
        return True

    def accept(self, sym):
        t = self.peak()
        if isinstance(sym, list) or isinstance(sym, dict) or isinstance(sym, set):
            if str(t) in sym:
                return self.consume()
            return False
        elif str(t) == sym:
            return self.consume()
        return False

    def expect_pattern(self, syms, description):
        match = self.match_pattern(syms)
        if match:
            return [self.accept(sym) for sym in syms]
        else:
            raise SyntaxError(description, None, self.lexer)

    def expect(self, sym, description):
        t = self.peak()
        if isinstance(sym, list) or isinstance(sym, dict) or isinstance(sym, set):
            if str(t) not in sym:
                raise SyntaxError(description, t, self.lexer)
        elif str(t) != sym:
            raise SyntaxError(description, t, self.lexer)
        return t

    def consume_whitespace(self):
        if self.has_next():
            while self.accept(' ') or self.accept('\n'):
                pass