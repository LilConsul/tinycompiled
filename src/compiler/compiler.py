from src.lexer import Lexer
from src.parser import Parser
from src.generator import NasmGenerator

def compile_tc_to_nasm(source_code: str) -> str:
    """Compile TinyCompiled source code to NASM assembly."""
    # Lexical analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Syntax analysis
    parser = Parser(tokens)
    ast = parser.parse()

    # Code generation
    generator = NasmGenerator()
    asm_code = generator.generate(ast)

    return asm_code
