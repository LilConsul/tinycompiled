from src.parser import Parser
from src.lexer import Lexer

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

print("Testing Lexer...")
lexer = Lexer(code)
tokens = lexer.tokenize()
print(f"Lexer produced {len(tokens)} tokens")

print("\nTesting Parser...")
parser = Parser(tokens)
ast = parser.parse()
print(f"Parser produced AST with {len(ast.statements)} statements")

print("\nAST Structure:")
for i, stmt in enumerate(ast.statements, 1):
    print(f"  {i}. {type(stmt).__name__}\t=\t{stmt}")
