from src.lexer.keyword import KEYWORD_DICT
from src.lexer.token import TokenType, Token


class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.s_len = len(source_code)

        self.pos = 0
        self.line = 1
        self.column = 1

        self.keywords = KEYWORD_DICT
        self.tokens = []

    def current_char(self):
        if self.pos >= self.s_len:
            return None
        return self.source[self.pos]

    def peek_char(self, offset=1):
        if self.pos + offset >= self.s_len:
            return None
        return self.source[self.pos + offset]

    def advance(self):
        if self.pos >= self.s_len:
            return

        if self.current_char() == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip_whitespace(self):
        while (
            self.current_char() is not None
            and self.current_char().isspace()
            and self.current_char() != "\n"
        ):
            self.advance()

    def skip_comment(self):
        if self.current_char() == ";":
            while self.current_char() is not None and self.current_char() != "\n":
                self.advance()

    def read_number(self) -> int:
        start_col = self.column
        num_str = ""

        # Handle negative numbers
        if self.current_char() == "-":
            num_str += "-"
            self.advance()

        # Hexadecimal
        if self.current_char() == "0" and self.peek_char() in "xX":
            self.advance()  # skip 0
            self.advance()  # skip x
            while (
                self.current_char() and self.current_char() in "0123456789abcdefABCDEF"
            ):
                num_str += self.current_char()
                self.advance()
            return int(num_str, 16) if num_str else 0

        # Binary
        if self.current_char() == "0" and self.peek_char() in "bB":
            self.advance()  # skip 0
            self.advance()  # skip b
            while self.current_char() and self.current_char() in "01":
                num_str += self.current_char()
                self.advance()
            return int(num_str, 2) if num_str else 0

        # Decimal
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()

        return int(num_str)

    def _tokenize_operators(self): ...

    def read_identifier(self):
        result = ""
        while self.current_char() and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            result += self.current_char()
            self.advance()
        return result

    def tokenize(self):
        while self.pos < self.s_len:
            self.skip_whitespace()
            current = self.current_char()

            if current is None:
                break

            if current == ";":
                self.skip_comment()
                continue

            if self.current_char() == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", self.line, self.column))
                self.advance()
                continue

            if self.current_char() == "\n":
                self.tokens.append(
                    Token(TokenType.NEWLINE, "\n", self.line, self.column)
                )
                self.advance()
                continue

            if self.current_char().isdigit() or (
                self.current_char() == "-"
                and self.peek_char()
                and self.peek_char().isdigit()
            ):
                num = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, num, self.line, self.column))
                continue

            self._tokenize_operators()

            if self.current_char().isalpha() or self.current_char() == "_":
                ident = self.read_identifier()

                # Check for label
                if self.current_char() == ":":
                    self.tokens.append(
                        Token(TokenType.LABEL, ident, self.line, self.column)
                    )
                    self.advance()  # skip :
                    continue

                # Check for register
                if ident in ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"]:
                    self.tokens.append(
                        Token(TokenType.REGISTER, ident, self.line, self.column)
                    )
                    continue

                # Check for keyword
                if ident.upper() in self.keywords:
                    self.tokens.append(
                        Token(
                            self.keywords[ident.upper()], ident, self.line, self.column
                        )
                    )
                    continue

                # Otherwise it's an identifier
                self.tokens.append(
                    Token(TokenType.IDENTIFIER, ident, self.line, self.column)
                )
                continue

            self.advance()
            # raise SyntaxError(
            #     f"Unexpected character '{current}' at line {self.line}, column {self.column}"
            # )

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


if __name__ == "__main__":
    code = """
    VAR x
    SET x, 10
    PRINT x
    ; This is a comment
    LOAD R1, 0x1A
    LOAD R2, 0b1010
    PRINT R1
    PRINT R2
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)