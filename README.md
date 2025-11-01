# TinyCompiled

**A Small Educational Compiler and Visualizer for Assembly Language Learning**

Authors: Denys Shevchenko, Yehor Karabanov

TinyCompiled is a small educational compiler and visualizer for a custom assembly-like language designed to help new developers understand the fundamentals of low-level programming, assembly language, and compilation. The project focuses on demonstrating how high-level instructions are translated into assembly code, providing an intuitive and interactive experience for learning and experimentation.

## Overview

TinyCompiled takes programs written in **TinyCompiled** (`.tc` files) — a simplified, human-readable assembly-like language — and translates them into real **x86-64 NASM assembly**, allowing users to see exactly how each instruction maps to low-level operations. By combining compilation with visualization, TinyCompiled bridges the gap between abstract programming concepts and the underlying machine instructions, making it a powerful tool for students, educators, and hobbyists.

## Key Features

### 🔄 TinyCompiled (.tc) → NASM Translation
TinyCompiled converts TinyCompiled instructions into NASM assembly line by line, including:
- Arithmetic operations (ADD, SUB, MUL, DIV)
- Logical/bitwise operations (AND, OR, XOR, NOT, SHL, SHR)
- Data movement (LOAD, SET, MOVE)
- Control flow (IF/ELSE, WHILE, FOR, LOOP, REPEAT/UNTIL)
- Functions (FUNC, CALL, RET)
- Input/output (PRINT, INPUT)
- Stack operations (PUSH, POP)
- Special instructions (HALT, NOP)

Each translation preserves the logical structure of the program, making it easy to follow and understand how high-level logic is implemented in assembly.

### 📊 Side-by-Side Visualization
Using the **Textualize/Textual** Python library, TinyCompiled displays TinyCompiled code alongside its NASM translation in a diff-style table. This visualization allows users to clearly see the mapping between abstract instructions and real machine operations, highlighting the effect of each line in an interactive terminal interface.

### 💻 CLI Interface
The command-line interface provides simple commands for:
- `tinycompiled compile INPUT_FILE [OUTPUT_FILE]` - Compile to NASM assembly (outputs to stdout if OUTPUT_FILE not provided)
- `tinycompiled build INPUT_FILE OUTPUT_FILE` - Compile to executable binary
- `tinycompiled run INPUT_FILE [--output OUTPUT_FILE]` - Compile and run program (temporary executable if OUTPUT_FILE not provided)

All commands support `--verbose` and `--debug` options for additional output.

### 🖥️ GUI Interface
The graphical interface provides:
- Real-time code editor for TinyCompiled
- Live compilation and preview of NASM output
- File save/load functionality
- Interactive terminal-based UI using Textual

### 📝 Language Features
TinyCompiled supports:
- **8 virtual registers**: R1-R8 (mapped to x86-64 registers)
- **Variables**: User-defined identifiers with optional initialization
- **Functions**: Named subroutines with parameters and return values
- **Control structures**: Loops, conditionals, and branching
- **I/O operations**: Print integers, read integers from stdin
- **Comments**: Semicolon-prefixed single-line comments
- **Literals**: Decimal, hexadecimal (0x), and binary (0b) numbers

## Architecture

### Compilation Pipeline

TinyCompiled follows a traditional compiler architecture:

1. **Lexical Analysis** (`src/lexer/`): Tokenizes source code into keywords, identifiers, numbers, and operators
2. **Syntax Analysis** (`src/parser/`): Parses tokens into an Abstract Syntax Tree (AST)
3. **Code Generation** (`src/generator/`): Translates AST into NASM x86-64 assembly code

### Virtual Registers

TinyCompiled provides 8 virtual registers that map to x86-64 registers:

- R1 → rax (accumulator)
- R2 → rbx (base)
- R3 → rcx (counter)
- R4 → rdx (data)
- R5 → rsi (source index)
- R6 → rdi (destination index)
- R7 → r8
- R8 → r9

### Memory Model

- **Variables**: Stored in the `.data` section with labels
- **Stack**: Used for function calls and local variables
- **Heap**: Not directly supported (assembly-level memory management)

## Example

### TinyCompiled (.tc) File

```assembly
; Simple arithmetic example
VAR x, 10
VAR y, 20

LOAD R1, x      ; Load x into R1
LOAD R2, y      ; Load y into R2
ADD R3, R1, R2  ; R3 = R1 + R2
PRINT R3        ; Print result
HALT
```

### Generated NASM Assembly

```nasm
section .data
    x dq 10
    y dq 20

section .text
    global _start

_start:
    mov rax, [x]      ; LOAD R1, x
    mov rbx, [y]      ; LOAD R2, y
    add rcx, rax      ; ADD R3, R1, R2
    add rcx, rbx
    mov rax, rcx      ; PRINT R3
    call print_int
    mov rax, 60       ; HALT
    xor rdi, rdi
    syscall

; Helper functions for I/O
print_int:
    ; ... (implementation details)
```

## Installation

### Prerequisites

- Python 3.14+
- NASM assembler (for building executables)
- LD linker (for building executables)

### Install from Source

```bash
git clone https://github.com/LilConsul/tinycompiled.git
cd tinycompiled
uv sync
```

### Dependencies

- `click>=8.3.0` - Command-line interface
- `textual[syntax]>=6.4.0` - Terminal user interface

## Usage

### CLI Usage

```bash
# Compile to NASM assembly
tinycompiled compile examples/fibonacci.tc output.asm

# Build executable
tinycompiled build examples/fibonacci.tc fibonacci

# Compile and run
tinycompiled run examples/fibonacci.tc
```

### GUI Usage

```bash
python main.py
```

This launches the interactive Textual-based editor where you can:
- Write TinyCompiled code in the left pane
- See real-time NASM translation in the right pane
- Save files with Ctrl+S
- Recompile with Ctrl+R

### Language Syntax

See `docs/DOCUMENTATION.md` for complete language reference.

## Project Structure

```
tinycompiled/
├── src/
│   ├── __init__.py
│   ├── compiler/
│   │   ├── compiler.py      # Main compilation pipeline
│   │   └── __init__.py
│   ├── lexer/
│   │   ├── lexer.py         # Lexical analyzer
│   │   ├── token.py         # Token definitions
│   │   ├── keyword.py       # Language keywords
│   │   └── __init__.py
│   ├── parser/
│   │   ├── parser.py        # Syntax analyzer
│   │   └── __init__.py
│   ├── ast/
│   │   ├── node.py          # AST node definitions
│   │   └── __init__.py
│   └── generator/
│       ├── nasm_generator.py # NASM code generator
│       └── __init__.py
├── examples/
│   ├── fibonacci.tc         # Fibonacci function example
│   └── ...
├── docs/
│   ├── DOCUMENTATION.md     # Language reference
│   └── USAGE.md             # Usage examples
├── cli.py                   # Command-line interface
├── main.py                  # GUI application
└── pyproject.toml           # Project configuration
```

## Project Goals

- **Educational Focus**: Help beginners understand assembly language and low-level programming concepts
- **Interactive Learning**: Provide real-time visualization of code translation
- **Accessibility**: Make assembly language learning approachable and engaging
- **Practical Knowledge**: Bridge the gap between high-level and low-level programming

## Contributing

Contributions are welcome! Areas for improvement:
- Additional language features (strings, arrays, floating-point)
- More sophisticated optimization passes
- Web-based interface
- Support for additional target architectures
- Enhanced error reporting and debugging

## License

This project is provided for educational purposes. Please refer to the repository for specific licensing information.

## References

- [GitHub Repository](https://github.com/LilConsul/tinycompiled)
- x86-64 Assembly Language Resources
- NASM Assembler Documentation
- Textual Framework Documentation
