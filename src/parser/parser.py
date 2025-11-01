from src.lexer import Token, TokenType
from src.ast.node import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.t_len = len(tokens)

        # Dispatch table: maps token types to parser methods
        self._statement_handlers = {
            TokenType.VAR: self.parse_var_decl,
            TokenType.LOAD: self.parse_load,
            TokenType.SET: self.parse_set,
            TokenType.PRINT: self.parse_print,
            TokenType.INPUT: self.parse_input,
        }

        # Simple statement handlers (no complex parsing)
        self._simple_handlers = {
            TokenType.HALT: lambda: Halt(),
            TokenType.NOP: lambda: Nop(),
        }

    def current_token(self) -> Token:
        if self.pos >= self.t_len:
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]

    def peek_token(self, offset=1) -> Token:
        if self.pos + offset >= self.t_len:
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos + offset]

    def advance(self):
        self.pos += 1

    def expect(self, expected: TokenType):
        token = self.current_token()
        if token.type != expected:
            raise SyntaxError(
                f"Expected token {expected}, but got {token.type} at line {token.line}, column {token.column}"
            )
        self.advance()
        return token

    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()

    def parse(self):
        ast = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                ast.append(stmt)
            self.skip_newlines()

        return Program(ast)

    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.current_token()
        token_type = token.type

        # Skip newlines
        if token_type == TokenType.NEWLINE:
            self.advance()
            return None

        # Check direct dispatch table
        if token_type in self._statement_handlers:
            return self._statement_handlers[token_type]()

        # Check simple handlers (HALT, NOP)
        if token_type in self._simple_handlers:
            self.advance()
            return self._simple_handlers[token_type]()

        # Control flow and structured statements
        if token_type == TokenType.LABEL:
            return self.parse_label()
        if token_type == TokenType.IF:
            return self.parse_if()
        if token_type == TokenType.LOOP:
            return self.parse_loop()
        if token_type == TokenType.WHILE:
            return self.parse_while()
        if token_type == TokenType.FOR:
            return self.parse_for()
        if token_type == TokenType.REPEAT:
            return self.parse_repeat()

        # Functions
        if token_type == TokenType.FUNC:
            return self.parse_function()
        if token_type == TokenType.CALL:
            return self.parse_call()
        if token_type == TokenType.RET:
            return self.parse_return()

        # Stack operations
        if token_type == TokenType.PUSH:
            return self.parse_push()
        if token_type == TokenType.POP:
            return self.parse_pop()

        # Register operations
        if token_type == TokenType.MOVE:
            return self.parse_move()
        if token_type == TokenType.NOT:
            return self.parse_not()

        # Binary operations
        if token_type in [
            TokenType.ADD,
            TokenType.SUB,
            TokenType.MUL,
            TokenType.DIV,
            TokenType.AND,
            TokenType.OR,
            TokenType.XOR,
        ]:
            return self.parse_binary_op()

        # Unary operations
        if token_type in [TokenType.INC, TokenType.DEC]:
            return self.parse_unary_op()

        # Shift operations
        if token_type in [TokenType.SHL, TokenType.SHR]:
            return self.parse_shift()

        raise SyntaxError(f"Unexpected token {token_type} at line {token.line}")

    def _parse_value(self, allowed_types=None):
        """
        Helper method to parse a value that can be a register, identifier, or number.
        Returns the parsed value.

        Args:
            allowed_types: List of allowed TokenTypes. If None, allows REGISTER, IDENTIFIER, NUMBER
        """
        if allowed_types is None:
            allowed_types = [TokenType.REGISTER, TokenType.IDENTIFIER, TokenType.NUMBER]

        token = self.current_token()

        if token.type in allowed_types:
            self.advance()
            return token.value

        # Build error message
        allowed_names = [t.name.lower() for t in allowed_types]
        expected = (
            ", ".join(allowed_names[:-1])
            + (" or " if len(allowed_names) > 1 else "")
            + allowed_names[-1]
        )
        raise SyntaxError(f"Expected {expected} at line {token.line}")

    def _parse_body(self, end_token: TokenType):
        """
        Helper method to parse a body of statements until an end token is reached.
        Returns a list of parsed statements.
        """
        body = []
        while self.current_token().type != end_token:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        return body

    def parse_var_decl(self) -> VarDecl:
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENTIFIER).value

        value = None
        if self.current_token().type == TokenType.COMMA:
            self.advance()
            value = self.expect(TokenType.NUMBER).value

        return VarDecl(name, value)

    def parse_load(self) -> Load:
        self.expect(TokenType.LOAD)
        dest = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        src = self._parse_value()
        return Load(dest, src)

    def parse_set(self) -> Set:
        self.expect(TokenType.SET)
        dest = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COMMA)
        src = self._parse_value([TokenType.REGISTER, TokenType.NUMBER])
        return Set(dest, src)

    def parse_move(self) -> Move:
        self.expect(TokenType.MOVE)
        dest = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        src = self.expect(TokenType.REGISTER).value
        return Move(dest, src)

    def parse_binary_op(self) -> BinaryOp:
        op_token = self.current_token()
        op = op_token.value.upper()
        self.advance()

        dest = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        left = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        right = self._parse_value([TokenType.REGISTER, TokenType.NUMBER])

        return BinaryOp(op, dest, left, right)

    def parse_unary_op(self) -> UnaryOp:
        op_token = self.current_token()
        op = op_token.value.upper()
        self.advance()
        operand = self._parse_value([TokenType.REGISTER, TokenType.IDENTIFIER])
        return UnaryOp(op, operand)

    def parse_not(self) -> UnaryOp:
        self.expect(TokenType.NOT)
        operand = self.expect(TokenType.REGISTER).value
        return UnaryOp("NOT", operand)

    def parse_shift(self) -> ShiftOp:
        op_token = self.current_token()
        op = op_token.value.upper()
        self.advance()

        dest = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        src = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        count = self.expect(TokenType.NUMBER).value

        return ShiftOp(op, dest, src, count)


    def parse_label(self) -> Label:
        label = self.expect(TokenType.LABEL).value
        return Label(label)

    def parse_function(self) -> Function:
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENTIFIER).value
        self.skip_newlines()
        body = self._parse_body(TokenType.ENDFUNC)
        self.expect(TokenType.ENDFUNC)
        return Function(name, body)

    def parse_call(self) -> Call:
        self.expect(TokenType.CALL)
        name = self.expect(TokenType.IDENTIFIER).value
        return Call(name)

    def parse_return(self) -> Return:
        self.expect(TokenType.RET)

        if self.current_token().type == TokenType.REGISTER:
            value = self.expect(TokenType.REGISTER).value
            return Return(value)

        return Return()

    def parse_condition(self) -> Condition:
        left = self._parse_value()

        op_token = self.current_token()
        if op_token.type in [
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
        ]:
            op = op_token.value
            self.advance()
        else:
            raise SyntaxError(f"Expected comparison operator at line {op_token.line}")

        right = self._parse_value()

        return Condition(left, op, right)

    def parse_loop(self) -> Loop:
        self.expect(TokenType.LOOP)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COMMA)
        limit = self.expect(TokenType.NUMBER).value
        self.skip_newlines()
        body = self._parse_body(TokenType.ENDLOOP)
        self.expect(TokenType.ENDLOOP)
        return Loop(var, limit, body)

    def parse_while(self) -> While:
        self.expect(TokenType.WHILE)
        condition = self.parse_condition()
        self.skip_newlines()
        body = self._parse_body(TokenType.ENDWHILE)
        self.expect(TokenType.ENDWHILE)
        return While(condition, body)

    def parse_for(self) -> For:
        self.expect(TokenType.FOR)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.FROM)
        start = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.TO)
        end = self.expect(TokenType.NUMBER).value

        step = 1
        if self.current_token().type == TokenType.STEP:
            self.advance()
            step = self.expect(TokenType.NUMBER).value

        self.skip_newlines()
        body = self._parse_body(TokenType.ENDFOR)
        self.expect(TokenType.ENDFOR)
        return For(var, start, end, step, body)

    def parse_repeat(self) -> Repeat:
        self.expect(TokenType.REPEAT)
        self.skip_newlines()
        body = self._parse_body(TokenType.UNTIL)
        self.expect(TokenType.UNTIL)
        condition = self.parse_condition()

        return Repeat(body, condition)

    def parse_if(self) -> If:
        self.expect(TokenType.IF)
        condition = self.parse_condition()
        self.skip_newlines()

        # Parse then body - need special handling for ELSE/ENDIF
        then_body = []
        while self.current_token().type not in [TokenType.ELSE, TokenType.ENDIF]:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
            self.skip_newlines()

        else_body = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.skip_newlines()
            else_body = self._parse_body(TokenType.ENDIF)

        self.expect(TokenType.ENDIF)
        return If(condition, then_body, else_body)

    def parse_push(self) -> Push:
        self.expect(TokenType.PUSH)
        register = self.expect(TokenType.REGISTER).value
        return Push(register)

    def parse_pop(self) -> Pop:
        self.expect(TokenType.POP)
        register = self.expect(TokenType.REGISTER).value
        return Pop(register)

    def parse_print(self) -> Print:
        self.expect(TokenType.PRINT)
        value = self._parse_value()
        return Print(value)

    def parse_input(self) -> Input:
        self.expect(TokenType.INPUT)
        dest = self._parse_value([TokenType.REGISTER, TokenType.IDENTIFIER])
        return Input(dest)
