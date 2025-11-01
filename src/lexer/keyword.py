from .token import TokenType

KEYWORD_DICT = {
    "VAR": TokenType.VAR,
    "LOAD": TokenType.LOAD,
    "SET": TokenType.SET,
    "MOVE": TokenType.MOVE,

    # BinaryOperations
    "ADD": TokenType.ADD,
    "SUB": TokenType.SUB,
    "MUL": TokenType.MUL,
    "DIV": TokenType.DIV,
    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "XOR": TokenType.XOR,

    # UnaryOperations
    "INC": TokenType.INC,
    "DEC": TokenType.DEC,
    "NOT": TokenType.NOT,

    "SHL": TokenType.SHL,
    "SHR": TokenType.SHR,

    "FUNC": TokenType.FUNC,
    "ENDFUNC": TokenType.ENDFUNC,
    "CALL": TokenType.CALL,
    "RET": TokenType.RET,
    # "LOOP": TokenType.LOOP,
    # "ENDLOOP": TokenType.ENDLOOP,
    # "WHILE": TokenType.WHILE,
    # "ENDWHILE": TokenType.ENDWHILE,
    # "FOR": TokenType.FOR,
    # "ENDFOR": TokenType.ENDFOR,
    # "FROM": TokenType.FROM,
    # "TO": TokenType.TO,
    # "STEP": TokenType.STEP,
    # "REPEAT": TokenType.REPEAT,
    # "UNTIL": TokenType.UNTIL,
    "IF": TokenType.IF,
    "ELSE": TokenType.ELSE,
    "ENDIF": TokenType.ENDIF,
    # "PUSH": TokenType.PUSH,
    # "POP": TokenType.POP,
    "PRINT": TokenType.PRINT,
    "INPUT": TokenType.INPUT,
    "HALT": TokenType.HALT,
    "NOP": TokenType.NOP,
}