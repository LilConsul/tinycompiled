from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    # Keywords
    VAR = auto()
    LOAD = auto()
    SET = auto()
    MOVE = auto()  # TODO
    ADD = auto()  # TODO
    SUB = auto()  # TODO
    MUL = auto()  # TODO
    DIV = auto()  # TODO
    INC = auto()  # TODO
    DEC = auto()  # TODO
    AND = auto()  # TODO
    OR = auto()  # TODO
    XOR = auto()  # TODO
    NOT = auto()  # TODO
    SHL = auto()  # TODO
    SHR = auto()  # TODO
    CMP = auto()  # TODO
    JMP = auto()  # TODO
    JE = auto()  # TODO
    JNE = auto()  # TODO
    JG = auto()  # TODO
    JL = auto()  # TODO
    JGE = auto()  # TODO
    JLE = auto()  # TODO
    FUNC = auto()  # TODO
    ENDFUNC = auto()  # TODO
    CALL = auto()  # TODO
    RET = auto()  # TODO
    LOOP = auto()  # TODO
    ENDLOOP = auto()  # TODO
    WHILE = auto()  # TODO
    ENDWHILE = auto()  # TODO
    FOR = auto()  # TODO
    ENDFOR = auto()  # TODO
    FROM = auto()  # TODO
    TO = auto()  # TODO
    STEP = auto()  # TODO
    REPEAT = auto()  # TODO
    UNTIL = auto()  # TODO
    IF = auto()  # TODO
    ELSE = auto()  # TODO
    ENDIF = auto()  # TODO
    PUSH = auto()  # TODO
    POP = auto()  # TODO
    PRINT = auto()
    INPUT = auto()
    HALT = auto()
    NOP = auto()

    # Literals and identifiers
    REGISTER = auto()  # R1, R2, etc.
    IDENTIFIER = auto()  # variable names
    NUMBER = auto()  # immediate values
    LABEL = auto()  # label:

    # Operators
    EQ = auto()  # ==
    NEQ = auto()  # !=
    GT = auto()  # >
    LT = auto()  # <
    GTE = auto()  # >=
    LTE = auto()  # <=

    # Punctuation
    COMMA = auto()
    COLON = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int