from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Keywords
    VAR = auto()
    LOAD = auto()
    SET = auto()
    # MOVE = auto()
    # ADD = auto()
    # SUB = auto()
    # MUL = auto()
    # DIV = auto()
    # INC = auto()
    # DEC = auto()
    # AND = auto()
    # OR = auto()
    # XOR = auto()
    # NOT = auto()
    # SHL = auto()
    # SHR = auto()
    # CMP = auto()
    # JMP = auto()
    # JE = auto()
    # JNE = auto()
    # JG = auto()
    # JL = auto()
    # JGE = auto()
    # JLE = auto()
    # FUNC = auto()
    # ENDFUNC = auto()
    # CALL = auto()
    # RET = auto()
    # LOOP = auto()
    # ENDLOOP = auto()
    # WHILE = auto()
    # ENDWHILE = auto()
    # FOR = auto()
    # ENDFOR = auto()
    # FROM = auto()
    # TO = auto()
    # STEP = auto()
    # REPEAT = auto()
    # UNTIL = auto()
    # IF = auto()
    # ELSE = auto()
    # ENDIF = auto()
    # PUSH = auto()
    # POP = auto()
    PRINT = auto()
    INPUT = auto()
    HALT = auto()
    NOP = auto()

    # Literals and identifiers
    REGISTER = auto()       # R1, R2, etc.
    IDENTIFIER = auto()     # variable names
    NUMBER = auto()         # immediate values
    # LABEL = auto()          # label:

    # Operators
    # EQ = auto()       # ==
    # NEQ = auto()      # !=
    # GT = auto()       # >
    # LT = auto()       # <
    # GTE = auto()      # >=
    # LTE = auto()      # <=

    # Punctuation
    COMMA = auto()
    COLON = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int