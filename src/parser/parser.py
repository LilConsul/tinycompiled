from src.lexer import Token, TokenType
from src.parser.node import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.t_len = len(tokens)

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

        if token.type == TokenType.VAR:
            return self.parse_var_decl()
        elif token.type == TokenType.LOAD:
            return self.parse_load()
        elif token.type == TokenType.SET:
            return self.parse_set()
        elif token.type == TokenType.MOVE:
            return self.parse_move()
        elif token.type in [
            TokenType.ADD,
            TokenType.SUB,
            TokenType.MUL,
            TokenType.DIV,
            TokenType.AND,
            TokenType.OR,
            TokenType.XOR,
        ]:
            return self.parse_binary_op()
        elif token.type in [TokenType.INC, TokenType.DEC]:
            return self.parse_unary_op()
        elif token.type == TokenType.NOT:
            return self.parse_not()
        elif token.type in [TokenType.SHL, TokenType.SHR]:
            return self.parse_shift()
        elif token.type == TokenType.CMP:
            return self.parse_compare()
        elif token.type in [
            TokenType.JMP,
            TokenType.JE,
            TokenType.JNE,
            TokenType.JG,
            TokenType.JL,
            TokenType.JGE,
            TokenType.JLE,
        ]:
            return self.parse_jump()
        elif token.type == TokenType.LABEL:
            return self.parse_label()
        elif token.type == TokenType.FUNC:
            return self.parse_function()
        elif token.type == TokenType.CALL:
            return self.parse_call()
        elif token.type == TokenType.RET:
            return self.parse_return()
        elif token.type == TokenType.LOOP:
            return self.parse_loop()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        elif token.type == TokenType.FOR:
            return self.parse_for()
        elif token.type == TokenType.REPEAT:
            return self.parse_repeat()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.PUSH:
            return self.parse_push()
        elif token.type == TokenType.POP:
            return self.parse_pop()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.INPUT:
            return self.parse_input()
        elif token.type == TokenType.HALT:
            self.advance()
            return Halt()
        elif token.type == TokenType.NOP:
            self.advance()
            return Nop()
        elif token.type == TokenType.NEWLINE:
            self.advance()
            return None
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

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

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            src = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            src = self.expect(TokenType.IDENTIFIER).value
        elif token.type == TokenType.NUMBER:
            src = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(
                f"Expected register, identifier or number at line {token.line}"
            )

        return Load(dest, src)

    def parse_set(self) -> Set:
        self.expect(TokenType.SET)
        dest = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COMMA)

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            src = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.NUMBER:
            src = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(f"Expected register or number at line {token.line}")

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

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            right = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.NUMBER:
            right = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(f"Expected register or number at line {token.line}")

        return BinaryOp(op, dest, left, right)

    def parse_unary_op(self) -> UnaryOp:
        op_token = self.current_token()
        op = op_token.value.upper()
        self.advance()

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            operand = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            operand = self.expect(TokenType.IDENTIFIER).value
        else:
            raise SyntaxError(f"Expected register or identifier at line {token.line}")

        return UnaryOp(op, operand)

    def parse_not(self) -> BinaryOp:
        self.expect(TokenType.NOT)
        dest = self.expect(TokenType.REGISTER).value
        self.expect(TokenType.COMMA)
        src = self.expect(TokenType.REGISTER).value
        # NOT is special - it has dest and src
        return BinaryOp("NOT", dest, src, 0)

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

    def parse_compare(self) -> Compare:
        self.expect(TokenType.CMP)

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            left = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            left = self.expect(TokenType.IDENTIFIER).value
        else:
            raise SyntaxError(f"Expected register or identifier at line {token.line}")

        self.expect(TokenType.COMMA)

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            right = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.NUMBER:
            right = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(f"Expected register or number at line {token.line}")

        return Compare(left, right)

    def parse_jump(self) -> Jump:
        op_token = self.current_token()
        op = op_token.value.upper()
        self.advance()
        label = self.expect(TokenType.IDENTIFIER).value
        return Jump(op, label)

    def parse_label(self) -> Label:
        label = self.expect(TokenType.LABEL).value
        return Label(label)

    def parse_function(self) -> Function:
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENTIFIER).value
        self.skip_newlines()

        body = []
        while self.current_token().type != TokenType.ENDFUNC:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

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
        token = self.current_token()
        if token.type == TokenType.REGISTER:
            left = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            left = self.expect(TokenType.IDENTIFIER).value
        elif token.type == TokenType.NUMBER:
            left = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(
                f"Expected register, identifier or number at line {token.line}"
            )

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

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            right = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            right = self.expect(TokenType.IDENTIFIER).value
        elif token.type == TokenType.NUMBER:
            right = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(
                f"Expected register, identifier or number at line {token.line}"
            )

        return Condition(left, op, right)

    def parse_loop(self) -> Loop:
        self.expect(TokenType.LOOP)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COMMA)
        limit = self.expect(TokenType.NUMBER).value
        self.skip_newlines()

        body = []
        while self.current_token().type != TokenType.ENDLOOP:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.ENDLOOP)
        return Loop(var, limit, body)

    def parse_while(self) -> While:
        self.expect(TokenType.WHILE)
        condition = self.parse_condition()
        self.skip_newlines()

        body = []
        while self.current_token().type != TokenType.ENDWHILE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

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

        body = []
        while self.current_token().type != TokenType.ENDFOR:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.ENDFOR)
        return For(var, start, end, step, body)

    def parse_repeat(self) -> Repeat:
        self.expect(TokenType.REPEAT)
        self.skip_newlines()

        body = []
        while self.current_token().type != TokenType.UNTIL:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.UNTIL)
        condition = self.parse_condition()

        return Repeat(body, condition)

    def parse_if(self) -> If:
        self.expect(TokenType.IF)
        condition = self.parse_condition()
        self.skip_newlines()

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
            else_body = []
            while self.current_token().type != TokenType.ENDIF:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                self.skip_newlines()

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

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            value = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            value = self.expect(TokenType.IDENTIFIER).value
        elif token.type == TokenType.NUMBER:
            value = self.expect(TokenType.NUMBER).value
        else:
            raise SyntaxError(
                f"Expected register, identifier or number at line {token.line}"
            )

        return Print(value)

    def parse_input(self) -> Input:
        self.expect(TokenType.INPUT)

        token = self.current_token()
        if token.type == TokenType.REGISTER:
            dest = self.expect(TokenType.REGISTER).value
        elif token.type == TokenType.IDENTIFIER:
            dest = self.expect(TokenType.IDENTIFIER).value
        else:
            raise SyntaxError(f"Expected register or identifier at line {token.line}")

        return Input(dest)
