# TinyCompiled

## **A Small Educational Compiler and Visualizer for Assembly Language Learning**

### **Authors:** Denys Shevchenko, Yehor Karabanov

![TinyCompiled GUI](img/coding.png)

TinyCompiled is a small educational compiler and visualizer for a custom assembly-like language designed to help new
developers understand the fundamentals of low-level programming, assembly language, and compilation. The project focuses
on demonstrating how high-level instructions are translated into assembly code, providing an intuitive and interactive
experience for learning and experimentation.

## 📖 Overview

TinyCompiled takes programs written in **TinyCompiled** (`.tc` files) — a simplified, human-readable assembly-like
language — and translates them into real **x86-64 NASM assembly**, allowing users to see exactly how each instruction
maps to low-level operations. By combining compilation with visualization, TinyCompiled bridges the gap between abstract
programming concepts and the underlying machine instructions, making it a powerful tool for students, educators, and
hobbyists.

## ✨ Key Features

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

Each translation preserves the logical structure of the program, making it easy to follow and understand how high-level
logic is implemented in assembly.

### 📊 Side-by-Side Visualization

Using the **Textualize/Textual** Python library, TinyCompiled displays TinyCompiled code alongside its NASM translation
in a diff-style table. This visualization allows users to clearly see the mapping between abstract instructions and real
machine operations, highlighting the effect of each line in an interactive terminal interface.

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

## 🏗️ Architecture

### 🔄 Compilation Pipeline

TinyCompiled follows a traditional compiler architecture:

1. **Lexical Analysis** (`src/lexer/`): Tokenizes source code into keywords, identifiers, numbers, and operators
2. **Syntax Analysis** (`src/parser/`): Parses tokens into an Abstract Syntax Tree (AST)
3. **Code Generation** (`src/generator/`): Translates AST into NASM x86-64 assembly code

### 🎯 Virtual Registers

TinyCompiled provides 8 virtual registers that map to x86-64 registers:

- R1 → rax (accumulator)
- R2 → rbx (base)
- R3 → rcx (counter)
- R4 → rdx (data)
- R5 → rsi (source index)
- R6 → rdi (destination index)
- R7 → r8
- R8 → r9

### 💾 Memory Model

- **Variables**: Stored in the `.data` section with labels
- **Stack**: Used for function calls and local variables
- **Heap**: Not directly supported (assembly-level memory management)

## 💡 Example

Here's a simple example demonstrating TinyCompiled syntax:

```assembly
; Calculate sum of numbers from 1 to 100
; Result: 5050

VAR n, 100
VAR sum, 0
VAR i, 1

WHILE i <= n
    LOAD R1, sum
    LOAD R2, i
    ADD R3, R1, R2
    SET sum, R3
    INC i
ENDWHILE

PRINT sum
HALT
```

**Run it:**

```bash
uv run cli.py run examples/sum.tc
# Output: 5050
```

**More Examples:**

Check the [`examples/`](examples/) directory for more demonstrations including:

- `fibonacci.tc` - Fibonacci sequence with functions
- `prime_check.tc` - Prime number checker
- `calculator.tc` - Interactive calculator
- `for_loop_demo.tc` - FOR loop variations
- `bitwise_demo.tc` - Bitwise operations
- And more!

## 📦 Installation

### ⚙️ Prerequisites

Before installing TinyCompiled, you need to install the following dependencies:

- **UV Package Manager** - [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- **NASM Assembler** (required for building/running programs) - [Install NASM](https://www.nasm.us/)
- **Linker (ld)** - Usually pre-installed on Linux/macOS. Windows users need WSL for the full build pipeline.

### 🔧 Install from Source

```bash
git clone https://github.com/LilConsul/tinycompiled.git
cd tinycompiled
uv sync
```

This will install all Python dependencies and set up the virtual environment.

## 🚀 Usage

### 💻 CLI Usage

Run TinyCompiled commands using `uv run`:

**Compile to NASM Assembly:**

```bash
uv run cli.py compile examples/sum.tc output.asm
```

Or output to stdout:

```bash
uv run cli.py compile examples/sum.tc
```

**Build Executable (Linux/macOS):**

```bash
uv run cli.py build examples/sum.tc sum_program
```

**Compile and Run:**

```bash
uv run cli.py run examples/sum.tc
```

**Verbose Output:**

```bash
uv run cli.py compile examples/fibonacci.tc --verbose
```

**Debug Mode (shows tokens and AST):**

```bash
uv run cli.py compile examples/fibonacci.tc --debug
```

### 🖥️ GUI Usage

Launch the interactive GUI editor:

```bash
uv run gui.py
```

![TinyCompiled GUI Interface](img/coding.png)

This launches the interactive Textual-based editor where you can:

- Write TinyCompiled code in the left pane
- Ctrl+R - See real-time NASM translation in the right pane
- Ctrl+S - Save files (shows file save dialog)
- Ctrl+Q - Quit the application

#### ⚡ GUI Features

**File Save Dialog:**

![Save Dialog](img/save-screen.png)

**Error Reporting:**

The GUI provides helpful error messages with line numbers and context:

![Error Message 1](img/error-msg.png)

![Error Message 2](img/error-msg-2.png)

### 📝 Language Syntax

See [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md) for complete language reference and [
`docs/DEFINITION.md`](docs/DEFINITION.md) for the formal language definition.

### 📋 Quick Reference

**Registers:** R1-R8 (mapped to x86-64 registers: rax, rbx, rcx, rdx, rsi, rdi, r8, r9)

**Variables:**

```assembly
VAR name, value    ; Declare and initialize
VAR count          ; Declare without initialization
```

**Arithmetic:**

```assembly
ADD R1, R2, R3     ; R1 = R2 + R3
SUB R1, R2, R3     ; R1 = R2 - R3
MUL R1, R2, R3     ; R1 = R2 * R3
DIV R1, R2, R3     ; R1 = R2 / R3
INC var            ; var++
DEC var            ; var--
```

**Bitwise Operations:**

```assembly
AND R1, R2, R3     ; R1 = R2 & R3
OR R1, R2, R3      ; R1 = R2 | R3
XOR R1, R2, R3     ; R1 = R2 ^ R3
NOT R1, R2         ; R1 = ~R2
SHL R1, R2, 2      ; R1 = R2 << 2
SHR R1, R2, 2      ; R1 = R2 >> 2
```

**Data Movement:**

```assembly
LOAD R1, var       ; Load variable into register
SET var, R1        ; Store register into variable
MOVE R1, R2        ; Copy R2 to R1
```

**Control Flow:**

```assembly
IF condition
    ; code
ELSE
    ; code
ENDIF

WHILE condition
    ; code
ENDWHILE

FOR var FROM start TO end
    ; code
ENDFOR

FOR var FROM start TO end STEP increment
    ; code
ENDFOR

LOOP count
    ; code
ENDLOOP

REPEAT
    ; code
UNTIL condition
```

**Functions:**

```assembly
FUNC function_name
    ; function body
    RET register
ENDFUNC

CALL function_name
```

**I/O:**

```assembly
PRINT register     ; Print integer value
INPUT variable     ; Read integer from stdin
```

**Stack:**

```assembly
PUSH register
POP register
```

**Other:**

```assembly
HALT              ; Exit program
NOP               ; No operation
; comment         ; Single-line comment
```

## 🏗️ Architecture

TinyCompiled is organized into modular components that reflect the typical stages of a compiler:

- **Lexer**: Tokenizes the input `.tc` source files into a stream of tokens.
- **Parser**: Analyzes the token stream and builds an Abstract Syntax Tree (AST).
- **AST**: Represents the program structure in a tree format for further processing.
- **Code Generator**: Converts the intermediate representation of AST into x86-64 NASM assembly code.
- **Compiler**: Coordinates the general compilation pipeline.
- **Visualizer/GUI**: Provides an interactive interface for users to write, compile, and visualize code execution.

Each component is organized in its own subdirectory within `src/`, promoting separation of concerns and ease of
maintenance.

## 📚 Documentation

For comprehensive documentation, see:

- [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md) - Complete language reference and usage guide
- [`docs/DEFINITION.md`](docs/DEFINITION.md) - Formal language definition with BNF grammar, semantic rules, and
  specifications

## 📁 Project Structure

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
│   ├── DEFINITION.md        # Formal language definition
│   └── USAGE.md             # Usage examples
├── cli.py                   # Command-line interface
├── gui.py                   # GUI application
└── pyproject.toml           # Project configuration
```

## 🎯 Project Goals

- **Educational Focus**: Help beginners understand assembly language and low-level programming concepts
- **Interactive Learning**: Provide real-time visualization of code translation
- **Accessibility**: Make assembly language learning approachable and engaging
- **Practical Knowledge**: Bridge the gap between high-level and low-level programming

## 💪 Our Implementation Experience

**Learning Through Building:**
This project represents our hands-on journey through compiler construction theory. Rather than following tutorials or using pre-built frameworks, we implemented every component from scratch based on academic textbooks (primarily Louden, 1997).

**What We Learned:**
- **Lexical Analysis**: Designed and implemented a complete tokenizer using finite automata principles
- **Parsing Theory**: Built a recursive descent parser from BNF grammar, understanding First/Follow sets
- **AST Construction**: Created hierarchical representations of program structure
- **Code Generation**: Translated high-level constructs to x86-64 assembly instructions
- **Error Handling**: Implemented meaningful error messages with context and line numbers

**Challenges Overcome:**
- Register allocation and management across nested control structures
- Label generation for loops and conditionals without conflicts
- Stack frame management for function calls
- Type checking and semantic validation before code generation
- Recursive descent parsing without backtracking

**Personal Growth:**
This project deepened our understanding of how programming languages work at a fundamental level. We can now read compiler textbooks with practical context, debug assembly code with confidence, and appreciate the complexity of production compilers. Most importantly, we learned that the best way to understand compiler theory is to implement one yourself.

**Why This Matters:**
Every software engineer should understand compilation at some level. Building TinyCompiled gave us insights into performance optimization, memory management, and low-level execution that inform our high-level programming decisions today.

## 📖 Theoretical Foundations

This language definition implements principles from compiler construction literature, particularly following the methodology described in Kenneth C. Louden's "Compiler Construction: Principles and Practice" (1997).

### Lexical Analysis (Compiler Phase 1)

The lexical structure described in our formal definition directly implements concepts from:

**Louden (1997), Chapter 2 - "Scanning":**
- **Section 2.2 (Regular Expressions)**: Token patterns for keywords, identifiers, and literals
- **Section 2.3 (Finite Automata)**: State-machine based token recognition
- **Section 2.4 (Implementation)**: Practical lexer implementation with lookahead

**Our Implementation:**
- Keywords: Reserved word recognition using hash table lookup (Louden pp. 49-51)
- Identifiers: Pattern `[a-zA-Z_][a-zA-Z0-9_]*` following Louden's identifier rules (p. 47)
- Number Literals: Support for decimal, hexadecimal, and binary as extended token types (Louden p. 52)
- Whitespace handling: Token separation following Louden's scanning principles (p. 44)

### Syntax Definition (Compiler Phase 2)

The BNF grammar notation and syntax rules follow:

**Louden (1997), Chapter 3 - "Context-Free Grammars and Parsing":**
- **Section 3.2 (BNF Notation)**: Extended BNF used throughout this specification (Louden pp. 83-87)
- **Section 3.3 (Parse Trees and ASTs)**: Our AST structure reflects Louden's abstract syntax design (pp. 90-94)
- **Section 3.5 (Grammar Types)**: LL(1) compatible grammar for recursive descent parsing (pp. 103-107)

**Louden (1997), Chapter 4 - "Top-Down Parsing":**
- **Section 4.3 (Recursive Descent)**: Our parser implements recursive descent without backtracking (pp. 131-138)
- **Section 4.4 (First and Follow Sets)**: Grammar designed with LL(1) properties (pp. 143-149)

**Aho et al. (2006), Chapter 4**: Syntax-directed translation schemes for code generation

**Our Implementation:**
- Control flow structures: Syntax designed for unambiguous parsing (Louden pp. 136-137)
- Statement sequences: Each statement clearly delimited for predictive parsing
- Expression grammar: Left-factored to avoid ambiguity (Louden p. 145)

### Semantic Rules (Compiler Phase 3)

Semantic constraints implement:

**Louden (1997), Chapter 6 - "Semantic Analysis":**
- **Section 6.2 (Symbol Tables)**: Variable and function name management (Louden pp. 253-262)
- **Section 6.3 (Data Types)**: Simplified type system with single integer type (pp. 263-271)
- **Section 6.4 (Type Checking)**: Declaration-before-use enforcement (pp. 272-280)

**Our Implementation:**
- Variable Declaration: Global scope symbol table following Louden pp. 255-258
- Function Scope: Function name uniqueness checking (Louden p. 259)
- Semantic Checks: Type consistency and name resolution as described in Louden Chapter 6

### Code Generation (Compiler Phase 4)

The compilation model targeting x86-64 NASM follows:

**Louden (1997), Chapter 8 - "Code Generation":**
- **Section 8.2 (Intermediate Code)**: AST serves as intermediate representation (Louden pp. 373-379)
- **Section 8.3 (Basic Code Generation)**: Template-based code generation for each AST node type (pp. 380-388)
- **Section 8.4 (Register Allocation)**: Simple register mapping strategy (pp. 389-396)
- **Section 8.5 (Code Generation for Control Flow)**: Label generation for loops and conditionals (pp. 397-405)

**Appel (2004), Chapters 6-7**: Modern compiler implementation techniques for x86-64 architecture

**Our Implementation:**
- Register Mapping: 8 virtual registers mapped to x86-64 hardware registers (Louden p. 390)
- Memory Layout: Standard .text, .data, .bss sections (Louden pp. 383-384)
- Control Flow Translation: Label-based implementation of jumps and branches (Louden pp. 401-403)
- Function Calls: Stack-based calling convention (Louden pp. 407-412)

### Implementation Methodology

This compiler was implemented following Louden's iterative development approach (Chapter 1, pp. 12-18):

1. **Lexical Analyzer**: Standalone tokenizer tested independently
2. **Parser**: Recursive descent parser built incrementally for each construct
3. **Semantic Analysis**: Symbol table and type checking added progressively
4. **Code Generator**: Template-based generation implemented per instruction type
5. **Testing**: Each phase validated with example programs before proceeding

This methodology ensured correctness at each compilation phase before integration, following best practices from Louden (1997) Chapter 1.4 "Compiler Structure".

## 📊 Comparison with Other Educational Compilers

### Educational Compiler Landscape Analysis

During our research phase, we studied numerous educational compiler projects to understand the state of the art in compiler pedagogy. We extensively referenced the [**Awesome Compilers**](https://github.com/aalhour/awesome-compilers) repository maintained by Ahmed Aalhour (@aalhour), which provides a comprehensive curated list of:

- Educational compiler implementations in various languages
- Academic papers and tutorials on compiler theory
- Links to textbooks and learning materials
- Examples of teaching compilers and language implementations

This resource helped us identify common patterns in educational compilers and, more importantly, recognize gaps that TinyCompiled addresses.

### Why TinyCompiled is Superior for Learning

After analyzing dozens of educational compiler projects, we designed TinyCompiled to overcome common limitations:

#### 1. **From-Scratch Implementation vs. Framework-Based**

**Most Educational Compilers:**
- Use LLVM, ANTLR, or other compiler-compiler tools
- Focus on high-level API usage rather than fundamental theory
- Students learn tool usage, not compiler principles

**TinyCompiled:**
- Every component (lexer, parser, code generator) implemented by us from first principles
- Direct application of textbook algorithms (Louden, 1997)
- Deep understanding gained through hands-on implementation
- Complete ownership of the codebase and design decisions

#### 2. **Real-Time Interactive Visualization**

**Most Educational Compilers:**
- Batch processing: compile → see output
- No intermediate step visualization
- Difficult to understand the compilation process

**TinyCompiled:**
- **Unique feature**: Side-by-side TUI showing source and NASM assembly simultaneously
- Instant visual feedback as you type (Ctrl+R to recompile)
- Color-coded diff-style interface for easy comparison
- See exactly how each instruction translates in real-time
- Makes the "invisible" compilation process visible and tangible

#### 3. **Practical Target Architecture**

**Many Educational Compilers:**
- Target virtual machines or custom bytecode
- Abstract away real hardware details
- Skills don't transfer to real-world systems programming

**TinyCompiled:**
- Generates real, executable x86-64 NASM assembly
- Teaches actual hardware register usage (rax, rbx, rcx, etc.)
- Students can run and debug their compiled programs on real hardware
- Direct applicability to systems programming, reverse engineering, and performance optimization
- Full support for modern 64-bit Linux/macOS systems

#### 4. **Beginner-Friendly Design**

**Many Educational Compilers:**
- Overwhelming feature sets (trying to be "production-ready")
- Complex syntax mimicking C/Java
- Steep learning curve for beginners

**TinyCompiled:**
- Simplified instruction set with only 8 intuitive registers (R1-R8)
- Assembly-like syntax that's easier to learn than raw x86-64
- Clear, explicit mapping between high-level constructs and machine code
- Comprehensive error messages with line numbers and context (not cryptic compiler errors)
- Each feature designed with pedagogy in mind, not feature completeness

#### 5. **Complete Academic Documentation**

**Many Educational Compilers:**
- Minimal documentation or informal READMEs
- No connection to compiler theory textbooks
- Missing formal language specifications

**TinyCompiled:**
- Formal BNF grammar specification ([DEFINITION.md](docs/DEFINITION.md))
- Complete mapping to Louden (1997) chapters and page numbers
- Professional academic documentation standards
- Explicit connection between implementation and theory
- Can be used as a companion to compiler textbooks

#### 6. **Dual Interface for Different Learning Styles**

**Most Educational Compilers:**
- CLI-only or web-only
- One-size-fits-all approach

**TinyCompiled:**
- CLI for scripting and automation (`cli.py`)
- Interactive GUI for visual learners (`gui.py`)
- Both interfaces provide the same powerful features
- Switch between modes based on task and preference

### Comparative Feature Matrix

| Feature | TinyCompiled | Typical Tutorial Compiler | LLVM-Based Educational Compiler |
|---------|--------------|---------------------------|----------------------------------|
| **From-Scratch Implementation** | ✅ Yes | ⚠️ Partial | ❌ No (uses LLVM) |
| **Real-Time Visualization** | ✅ Side-by-side TUI | ❌ Batch only | ❌ Batch only |
| **Real Hardware Target** | ✅ x86-64 NASM | ❌ Virtual machine | ✅ Via LLVM |
| **Beginner-Friendly Syntax** | ✅ Simplified ASM-like | ⚠️ C-like (complex) | ⚠️ C-like (complex) |
| **Formal Specification** | ✅ Full BNF grammar | ❌ Informal | ⚠️ Partial |
| **Theory-to-Code Mapping** | ✅ Explicit (Louden refs) | ❌ None | ❌ Framework-focused |
| **GUI + CLI** | ✅ Both | ❌ Usually one | ⚠️ CLI only |
| **Complete Toolchain** | ✅ Compile + assemble + run | ⚠️ Compile only | ✅ Via LLVM |
| **Educational Documentation** | ✅ Extensive | ❌ Minimal | ⚠️ Tool-focused |

### Our Educational Impact

Unlike passive tutorial-following or framework-based projects, TinyCompiled represents **genuine compiler construction learning through implementation**. We didn't just use existing tools — we built the tools themselves, gaining deep insight into:

- Lexical analysis and finite automata
- Parsing theory and LL(1) grammars
- AST construction and tree traversal
- Code generation and register allocation
- Symbol table management
- Error handling and recovery

This hands-on approach to learning compiler construction cannot be replicated by using high-level frameworks or following step-by-step tutorials. TinyCompiled demonstrates that the best way to understand compilers is to **build one from scratch**.

## 📚 Documentation Links

- [Language Documentation](docs/DOCUMENTATION.md) - Complete guide and examples
- [Formal Definition](docs/DEFINITION.md) - BNF grammar and language specification

## 📄 License

This project is provided for educational purposes. Please refer to the repository for specific licensing information.

## 📖 Academic References

### Primary Textbooks

1. **Louden, K. C.** (1997). *Compiler Construction: Principles and Practice*. PWS Publishing Company.
   - **Primary theoretical foundation for this implementation**
   - Chapter 2: Scanning (Lexical Analysis)
   - Chapters 3-4: Context-Free Grammars and Top-Down Parsing
   - Chapter 6: Semantic Analysis and Symbol Tables
   - Chapter 8: Code Generation for Assembly Language Targets

2. **Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D.** (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.
   - Known as the "Dragon Book" - foundational compiler theory reference
   - Used for syntax-directed translation and intermediate representations

3. **Appel, A. W.** (2004). *Modern Compiler Implementation in C*. Cambridge University Press.
   - Modern techniques for x86-64 code generation and register allocation

### Related Resources

4. **Aalhour, A.** *Awesome Compilers - A curated list of awesome resources on Compilers, Interpreters and Runtimes*. GitHub Repository. https://github.com/aalhour/awesome-compilers (accessed November 2025)
   - Comprehensive collection of educational compiler resources
   - Used during research phase to study existing educational compilers
   - Helped identify gaps in compiler pedagogy that TinyCompiled addresses

### Technical References

5. **Intel Corporation** (2023). *Intel® 64 and IA-32 Architectures Software Developer's Manual*.
   - Official x86-64 instruction set architecture reference

6. **NASM Development Team** (2023). *NASM - The Netwide Assembler Documentation*.
   - Target assembly language syntax and directives

**See [Theoretical Foundations](#-theoretical-foundations) section above for detailed mapping between this implementation and academic sources.**

## 🔗 Technical References

- [GitHub Repository](https://github.com/LilConsul/tinycompiled)
- [NASM Assembler Documentation](https://www.nasm.us/docs.html) - Target assembly language specification
- [Textual Framework Documentation](https://textual.textualize.io/) - GUI implementation framework
- [x86-64 ABI Reference](https://refspecs.linuxfoundation.org/elf/x86_64-abi-0.99.pdf) - Calling conventions and register usage
