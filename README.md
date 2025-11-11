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

### 🧩 Modular Components

TinyCompiled is organized into modular components that reflect the typical stages of a compiler:

- **Lexer** (`src/lexer/`): Tokenizes the input `.tc` source files into a stream of tokens
- **Parser** (`src/parser/`): Analyzes the token stream and builds an Abstract Syntax Tree (AST)
- **AST** (`src/ast/`): Represents the program structure in a tree format for further processing
- **Code Generator** (`src/generator/`): Converts the intermediate representation of AST into x86-64 NASM assembly code
- **Compiler** (`src/compiler/`): Coordinates the overall compilation pipeline
- **GUI** (`gui.py`): Provides an interactive Textual-based interface for users to write, compile, and visualize code execution

Each component is organized in its own subdirectory within `src/`, promoting separation of concerns and ease of maintenance.

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
│   └── DEFINITION.md        # Formal language definition
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

## 🔧 Real Implementation Challenges & Solutions

Building TinyCompiled from scratch meant facing real compiler design problems. Here are the key challenges we encountered and how academic literature helped us solve them:

### Challenge 1: Distinguishing Negative Numbers from Subtraction Operator

**The Problem:**
When implementing the lexer, we faced ambiguity: how do you know if `-` is a subtraction operator or part of a negative number literal like `-42`?

```python
# Initial naive approach would fail on:
LOAD R1, -10    # Is this "LOAD R1 , - 10" or "LOAD R1 , -10"?
SUB R2, R1, 5   # This works fine
```

**The Solution:**
Consulted **Louden (1997), Chapter 2.4 "Implementation of a Scanner"** (pp. 52-54), which discusses lookahead techniques. We implemented character lookahead using `peek_char()`:

```python
def read_number(self):
    # Handle negative numbers with lookahead
    if self.current_char() == "-":
        num_str += "-"
        self.advance()
    # ... rest of number parsing
```

This solved the ambiguity by checking if `-` is followed by a digit in the lexer context.

### Challenge 2: Supporting Multiple Number Formats (Decimal, Hex, Binary)

**The Problem:**
Assembly programmers expect to write numbers in different bases: `255`, `0xFF`, `0b11111111`. How do we parse all three without conflicts?

**The Solution:**
**Louden (1997), Section 2.2 "Regular Expressions"** (pp. 47-49) and **Fischer & LeBlanc "Crafting a Compiler" Chapter 3** taught us about prefix-based disambiguation. We implemented a two-character lookahead strategy:

```python
# Check for "0x" prefix → hexadecimal
if self.current_char() == "0" and self.peek_char() in "xX":
    # parse hex digits
    return int(num_str, 16)

# Check for "0b" prefix → binary  
if self.current_char() == "0" and self.peek_char() in "bB":
    # parse binary digits
    return int(num_str, 2)

# Otherwise → decimal
```

### Challenge 3: Nested Control Structures and Unique Label Generation

**The Problem:**
When generating assembly for nested loops and conditionals, labels must be unique to avoid conflicts:

```assembly
IF x > 0
    WHILE y < 10
        IF z == 5
            PRINT z
        ENDIF
    ENDWHILE
ENDIF
```

This generates multiple labels like `if_start`, `while_start`, `if_end` - but which `if_end` belongs to which `IF`?

**The Solution:**
**Louden (1997), Chapter 8.5 "Code Generation for Control Statements"** (pp. 401-405) describes using a global counter for unique labels. We implemented:

```python
def generate_if(self, stmt: If):
    else_label = f"else_{self.label_counter}"
    endif_label = f"endif_{self.label_counter}"
    self.label_counter += 1  # Ensure uniqueness!
    
    # Generate jump logic...
```

Each control structure increments the counter, guaranteeing unique labels even in deeply nested code.

### Challenge 4: Handling Bidirectional FOR Loops

**The Problem:**
Our `FOR` loop needed to work in both directions:
```
FOR i FROM 1 TO 10 STEP 1     # Ascending
FOR i FROM 10 TO 1 STEP -1    # Descending
```

The exit condition changes based on step direction - ascending loops need `>` comparison, descending need `<`.

**The Solution:**
**Appel (2004), "Modern Compiler Implementation"** Chapter 7 discusses direction-aware loop generation. We adapted it:

```python
def generate_for(self, stmt: For):
    # ...
    if stmt.step > 0:
        # Ascending: exit when var > end
        self.emit(f"jg {end_label}")
    else:
        # Descending: exit when var < end
        self.emit(f"jl {end_label}")
```

### Challenge 5: Register Allocation for Condition Evaluation

**The Problem:**
Conditional expressions like `IF R1 > R2` need temporary registers to perform comparison without clobbering user data. Which registers are safe to use?

**The Solution:**
**Louden (1997), Section 8.4 "Register Allocation"** (pp. 389-396) discusses reserving temporary registers. We reserved `r10` and `r11` (not in our R1-R8 virtual set) for internal use:

```python
def generate_condition(self, cond: Condition, false_label: str):
    # Load operands into reserved temporary registers
    self.emit(f"mov r10, {self.get_register(cond.left)}")
    self.emit(f"mov r11, {self.get_register(cond.right)}")
    self.emit("cmp r10, r11")
    # Jump based on condition...
```

This prevents corrupting user registers R1-R8 during comparisons.

### Challenge 6: Recursive Descent Parser Structure

**The Problem:**
How do you structure a parser that handles statements like `IF`, `WHILE`, `FOR` without getting confused about which `END` keyword closes which block?

**The Solution:**
**Louden (1997), Chapter 4.3 "Recursive Descent Parsing"** (pp. 131-138) and **Fischer & LeBlanc "Crafting a Compiler" Chapter 5** taught us to use recursive methods with explicit termination conditions:

```python
def parse_if(self) -> If:
    self.expect(TokenType.IF)
    condition = self.parse_condition()
    
    # Parse until we hit ELSE or ENDIF
    then_body = []
    while self.current_token().type not in [TokenType.ELSE, TokenType.ENDIF]:
        then_body.append(self.parse_statement())
    
    # Handle optional ELSE...
    self.expect(TokenType.ENDIF)  # Explicit termination
```

Each control structure method knows exactly which token terminates it, preventing mismatched blocks.

### What We Learned

These weren't textbook exercises - they were real bugs and design decisions we faced while building TinyCompiled. Each time we hit a wall, we:

1. **Identified the specific problem** (ambiguous parsing, label conflicts, etc.)
2. **Consulted compiler theory books** (Louden, Appel, Fischer & LeBlanc)
3. **Adapted the theoretical solution** to our assembly-like language design
4. **Tested with real examples** until it worked correctly

This hands-on problem-solving process taught us more about compiler construction than any tutorial could. The books didn't give us copy-paste code - they gave us **design patterns and principles** that we adapted to our specific challenges.

## 📊 Comparison with Other Educational Compilers

### Educational Compiler Landscape Analysis

During our research phase, we studied numerous educational compiler projects to understand the state of the art in compiler pedagogy. We extensively referenced the [**Awesome Compilers**](https://github.com/aalhour/awesome-compilers) repository maintained by Ahmed Aalhour (@aalhour), which provides a comprehensive curated list of:

- Educational compiler implementations in various languages
- Academic papers and tutorials on compiler theory
- Links to textbooks and learning materials
- Examples of teaching compilers and language implementations

This resource helped us identify common patterns in educational compilers and, more importantly, recognize gaps that TinyCompiled addresses.

### Why TinyCompiled is Superior for Learning

After analyzing educational compiler projects, we designed TinyCompiled to overcome common limitations:

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
- Batch processing: compile and view the output
- No intermediate step visualization
- Difficult to understand the compilation process

**TinyCompiled:**
- **Unique feature**: Side-by-side TUI showing source and NASM assembly simultaneously
- Instant visual feedback as you type (Ctrl+R to recompile)
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
- Explicit connection between implementation and theory
- Can be used as a companion to compiler textbooks

#### 6. **Dual Interface for Different Learning Styles**

**Most Educational Compilers:**
- CLI-only or web-only
- One-size-fits-all approach

**TinyCompiled:**
- CLI for scripting and automation (`cli.py`)
- Interactive GUI for visual learners (`gui.py`)
- Both interfaces provide the same features
- Switch between modes based on task and preference

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

## 📖 Academic References

### Primary Textbooks

1. **Louden, K. C.** (1997). *Compiler Construction: Principles and Practice*. PWS Publishing Company.

2. **Fischer, C. N., & LeBlanc, R. J.** (1991). *Crafting a Compiler*. Benjamin/Cummings Publishing.

3. **Appel, A. W.** (2004). *Modern Compiler Implementation in C*. Cambridge University Press.

4. **Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D.** (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.

### Related Resources

5. **Aalhour, A.** *Awesome Compilers - A curated list of awesome resources on Compilers, Interpreters and Runtimes*. GitHub Repository. https://github.com/aalhour/awesome-compilers (accessed October 2025)

### Technical References

6. **Intel Corporation** (2023). *Intel® 64 and IA-32 Architectures Software Developer's Manual*.
   - Official x86-64 instruction set architecture reference

7. **NASM Development Team** (2023). *NASM - The Netwide Assembler Documentation*.
   - Target assembly language syntax and directives

**See [Real Implementation Challenges & Solutions](#-real-implementation-challenges--solutions) section above for specific examples of how we applied these textbooks to solve practical problems.**

## 🔗 Technical References

- [GitHub Repository](https://github.com/LilConsul/tinycompiled)
- [NASM Assembler Documentation](https://www.nasm.us/docs.html) - Target assembly language specification
- [Textual Framework Documentation](https://textual.textualize.io/) - GUI implementation framework
- [x86-64 ABI Reference](https://refspecs.linuxfoundation.org/elf/x86_64-abi-0.99.pdf) - Calling conventions and register usage

## 📄 License

This project is provided for educational purposes. Please refer to the repository for specific licensing information.
