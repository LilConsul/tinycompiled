import os
from src.lexer import Lexer
from src.parser import Parser
from src.generator import NasmGenerator


def compile_tc_to_nasm(source_code: str) -> str:
    """Compile TinyCompiled source code to NASM assembly."""
    debug = os.environ.get('DEBUG', '').lower() in ('true', '1', 'yes')

    # Lexical analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if debug:
        print("=== TOKENS ===")
        for token in tokens:
            print(f"  {token}")
        print()

    # Syntax analysis
    parser = Parser(tokens)
    ast = parser.parse()

    if debug:
        print("=== AST ===")
        print(f"Program(")
        print(f"  statements=[")
        for i, stmt in enumerate(ast.statements):
            comma = "," if i < len(ast.statements) - 1 else ""
            print(f"    {stmt}{comma}")
        print(f"  ]")
        print(f")")
        print()

    # Code generation
    generator = NasmGenerator()
    asm_code = generator.generate(ast)

    return asm_code
