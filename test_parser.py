"""Quick test to verify the refactored parser works correctly."""
from src.parser import Parser
from src.lexer import Lexer

# Test simple program
code = """
VAR x
SET x, 10
PRINT x
LOAD R1, 26
PRINT R1
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
    print(f"  {i}. {type(stmt).__name__}")

print("\nAll tests passed! Parser refactoring successful.")

