from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    WORD = auto()
    STRING = auto()
    NUMBER = auto()
    PERIOD = auto()
    COMMA = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in " \t\r":
            self.advance()

    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        self.advance()  # skip opening quote
        result = []
        while self.pos < len(self.source):
            ch = self.peek()
            if ch == "\\":
                self.advance()
                escaped = self.advance() if self.pos < len(self.source) else ""
                escape_map = {"n": "\n", "t": "\t", "\\": "\\", '"': '"'}
                result.append(escape_map.get(escaped, escaped))
            elif ch == '"':
                self.advance()  # skip closing quote
                return Token(TokenType.STRING, "".join(result), start_line, start_col)
            elif ch == "\n":
                raise LexerError("Unterminated string", self.line, self.column)
            else:
                result.append(self.advance())
        raise LexerError("Unterminated string", self.line, self.column)

    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        result = []
        has_dot = False
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isdigit():
                result.append(self.advance())
            elif ch == "." and not has_dot:
                has_dot = True
                result.append(self.advance())
            else:
                break
        return Token(TokenType.NUMBER, "".join(result), start_line, start_col)

    def read_word(self) -> Token:
        start_line = self.line
        start_col = self.column
        result = []
        while self.pos < len(self.source):
            ch = self.peek()
            if ch and (ch.isalnum() or ch == "_"):
                result.append(self.advance())
            else:
                break
        return Token(TokenType.WORD, "".join(result), start_line, start_col)

    def tokenize(self) -> list:
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break

            ch = self.peek()

            if ch == '"':
                self.tokens.append(self.read_string())
            elif ch == ".":
                line, col = self.line, self.column
                self.advance()
                self.tokens.append(Token(TokenType.PERIOD, ".", line, col))
            elif ch == ",":
                line, col = self.line, self.column
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ",", line, col))
            elif ch == "\n":
                line, col = self.line, self.column
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, "\n", line, col))
            elif ch.isdigit():
                self.tokens.append(self.read_number())
            elif ch.isalpha() or ch == "_":
                self.tokens.append(self.read_word())
            else:
                raise LexerError(f"Unexpected character: {ch!r}", self.line, self.column)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
