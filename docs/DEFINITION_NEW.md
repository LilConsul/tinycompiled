# TinyCompiled Language Formal Definition

**Version:** 1.0  
**Date:** November 2025  
**Authors:** Yehor Karabanov, Denys Shevchenko

---

## 1. Introduction

### 1.1 Overview

TinyCompiled is an educational assembly-like programming language that compiles to x86-64 NASM assembly. It provides a simplified instruction set designed to teach compiler construction and low-level programming concepts without the complexity of full x86-64 assembly.

### 1.2 Theoretical Foundation

This language definition and compiler implementation are based on principles from **Kenneth C. Louden's "Compiler Construction: Principles and Practice"** (PWS Publishing, 1997). Our implementation follows the traditional compiler phases as outlined in Louden's textbook:

- **Chapter 1 (Introduction)**: Overall compiler structure and phases (pp. 1-28)
- **Chapter 2 (Scanning)**: Lexical analysis and finite automata (pp. 29-80)
- **Chapter 3 (Context-Free Grammars)**: Syntax specification using BNF (pp. 81-130)
- **Chapter 4 (Top-Down Parsing)**: Recursive descent parser implementation (pp. 131-172)
- **Chapter 6 (Semantic Analysis)**: Symbol tables and type checking (pp. 249-302)
- **Chapter 8 (Code Generation)**: Assembly code generation techniques (pp. 361-420)

### 1.3 Implementation Approach

Following Louden's methodology (Chapter 1.4, pp. 12-18), we implemented the compiler in distinct phases:

1. **Lexical Analyzer** (`src/lexer/lexer.py`): Tokenizes source code using finite state machines
2. **Parser** (`src/parser/parser.py`): Builds Abstract Syntax Tree using recursive descent
3. **Code Generator** (`src/generator/nasm_generator.py`): Generates x86-64 NASM assembly

Each phase was developed and tested independently before integration, ensuring correctness at every step.

---

## 2. Lexical Structure

### 2.1 Lexical Analysis Theory (Louden Chapter 2)

The lexical analyzer implements a **finite state machine** (Louden Section 2.3, pp. 44-52) that recognizes tokens through pattern matching. Our implementation uses:

- **Regular expressions** for token pattern specification (Louden 2.2, pp. 34-44)
- **Lookahead buffering** for multi-character operators (Louden 2.5, pp. 65-70)
- **Hash table** for keyword recognition (Louden 2.2, pp. 49-51)

**Implementation Details:**
```python
# src/lexer/lexer.py - Line-by-line scanning with position tracking
class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0          # Current position
        self.line = 1         # Line number for error reporting
        self.column = 1       # Column number for error reporting
        self.keywords = KEYWORD_DICT  # Hash table for O(1) keyword lookup
```

### 2.2 Character Set

TinyCompiled source code is written in **ASCII** or **UTF-8** encoding.

**Allowed characters:**
- Letters: `a-z`, `A-Z`
- Digits: `0-9`
- Special: `_`, `,`, `:`, `;`, `-`, `=`, `!`, `>`, `<`
- Whitespace: space, tab, newline

### 2.3 Token Classification

Following Louden's token classification (Section 2.2, pp. 32-34), TinyCompiled tokens fall into these categories:

#### 2.3.1 Keywords (Reserved Words)

**Lexical Rule:** Keywords are **case-insensitive** and recognized through hash table lookup.

**Implementation:** (Louden pp. 49-51 - Hash table for keyword recognition)
```python
# src/lexer/keyword.py
KEYWORD_DICT = {
    "VAR": TokenType.VAR,
    "LOAD": TokenType.LOAD,
    # ... 40+ keywords
}
```

**Complete Keyword List:**
```
Data Movement:    VAR, LOAD, SET, MOVE
Arithmetic:       ADD, SUB, MUL, DIV, INC, DEC
Bitwise:          AND, OR, XOR, NOT, SHL, SHR
Control Flow:     IF, ELSE, ENDIF, WHILE, ENDWHILE, FOR, ENDFOR, 
                  FROM, TO, STEP, LOOP, ENDLOOP, REPEAT, UNTIL
Functions:        FUNC, ENDFUNC, CALL, RET
Stack:            PUSH, POP
I/O:              PRINT, INPUT
Special:          HALT, NOP
```

#### 2.3.2 Registers

**Lexical Rule:** Register names are **case-sensitive** and must match exactly: `R1`, `R2`, ..., `R8`

**Pattern:** `R[1-8]`

**Implementation:**
```python
# src/lexer/lexer.py - Line 175
if ident in ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"]:
    self.tokens.append(Token(TokenType.REGISTER, ident, self.line, self.column))
```

**Mapping to x86-64 Architecture:**
| Virtual | Physical x86-64 | Purpose (System V ABI) |
|---------|----------------|------------------------|
| R1      | rax            | Accumulator, return value |
| R2      | rbx            | Base register |
| R3      | rcx            | Counter register |
| R4      | rdx            | Data register |
| R5      | rsi            | Source index |
| R6      | rdi            | Destination index |
| R7      | r8             | General purpose |
| R8      | r9             | General purpose |

#### 2.3.3 Identifiers

**BNF Grammar:** (Following Louden Section 3.2, pp. 83-87)
```bnf
identifier ::= (letter | '_') (letter | digit | '_')*
letter     ::= 'a'..'z' | 'A'..'Z'
digit      ::= '0'..'9'
```

**Properties:**
- **Case-sensitive**: `counter` ≠ `Counter`
- **Must start** with letter or underscore
- **Cannot be** a keyword or register name
- **Unlimited length** (implementation-dependent)

**Valid Examples:**
```
myVar, counter, sum_total, _temp, value123, camelCase
```

**Invalid Examples:**
```
123var    (starts with digit)
my-var    (contains hyphen)
R1        (reserved register name)
WHILE     (reserved keyword)
```

**Implementation:** (Louden pp. 47-48 - Identifier recognition)
```python
# src/lexer/lexer.py - read_identifier()
def read_identifier(self):
    result = ""
    while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
        result += self.current_char()
        self.advance()
    return result
```

#### 2.3.4 Number Literals

TinyCompiled supports three number formats, following extended token types (Louden p. 52):

**1. Decimal (Base 10):**
```bnf
decimal ::= '-'? digit+
```
Examples: `42`, `-10`, `0`, `999`

**2. Hexadecimal (Base 16):**
```bnf
hexadecimal ::= '-'? '0' ('x' | 'X') hexdigit+
hexdigit    ::= digit | 'a'..'f' | 'A'..'F'
```
Examples: `0xFF`, `0x2A`, `-0x10`, `0xDEADBEEF`

**3. Binary (Base 2):**
```bnf
binary ::= '-'? '0' ('b' | 'B') ('0' | '1')+
```
Examples: `0b1010`, `0b11111111`, `-0b101`

**Implementation:** (Louden Section 2.3, pp. 52-55 - Multi-base number recognition)
```python
# src/lexer/lexer.py - read_number()
def read_number(self) -> int:
    num_str = ""
    
    # Handle negative sign
    if self.current_char() == "-":
        num_str += "-"
        self.advance()
    
    # Hexadecimal: 0x...
    if self.current_char() == "0" and self.peek_char() in "xX":
        self.advance()  # skip 0
        self.advance()  # skip x
        while self.current_char() and self.current_char() in "0123456789abcdefABCDEF":
            num_str += self.current_char()
            self.advance()
        return int(num_str, 16)
    
    # Binary: 0b...
    if self.current_char() == "0" and self.peek_char() in "bB":
        self.advance()  # skip 0
        self.advance()  # skip b
        while self.current_char() and self.current_char() in "01":
            num_str += self.current_char()
            self.advance()
        return int(num_str, 2)
    
    # Decimal (default)
    while self.current_char() and self.current_char().isdigit():
        num_str += self.current_char()
        self.advance()
    
    return int(num_str)
```

#### 2.3.5 Comparison Operators

**Token Recognition:** Multi-character operators require **lookahead** (Louden Section 2.5, pp. 65-70)

| Operator | Token Type | Meaning |
|----------|-----------|---------|
| `==`     | EQ        | Equal to |
| `!=`     | NEQ       | Not equal to |
| `>`      | GT        | Greater than |
| `<`      | LT        | Less than |
| `>=`     | GTE       | Greater than or equal |
| `<=`     | LTE       | Less than or equal |

**Implementation:** (Two-character lookahead)
```python
# src/lexer/lexer.py - Line 120-135
if self.current_char() == "=" and self.peek_char() == "=":
    self.tokens.append(Token(TokenType.EQ, "==", self.line, self.column))
    self.advance()
    self.advance()
    continue

if self.current_char() == "!" and self.peek_char() == "=":
    self.tokens.append(Token(TokenType.NEQ, "!=", self.line, self.column))
    self.advance()
    self.advance()
    continue
```

#### 2.3.6 Punctuation and Delimiters

| Symbol | Token Type | Purpose |
|--------|-----------|---------|
| `,`    | COMMA     | Argument separator |
| `:`    | COLON     | Label marker (reserved) |
| `\n`   | NEWLINE   | Statement terminator |
| `;`    | (comment) | Single-line comment prefix |

**Comments:** Following Louden pp. 44-45, comments are **not tokenized** but skipped during scanning.

```python
# src/lexer/lexer.py - skip_comment()
def skip_comment(self):
    if self.current_char() == ";":
        while self.current_char() is not None and self.current_char() != "\n":
            self.advance()
```

**Example:**
```assembly
VAR x, 10    ; This is a comment
PRINT x      ; Comments extend to end of line
```

#### 2.3.7 Whitespace Handling

**Rule:** Spaces and tabs are **ignored** except as token separators (Louden p. 44).

**Newlines are significant:** They serve as statement terminators in the grammar.

```python
# src/lexer/lexer.py - skip_whitespace()
def skip_whitespace(self):
    while (self.current_char() is not None 
           and self.current_char().isspace() 
           and self.current_char() != "\n"):  # Preserve newlines!
        self.advance()
```

### 2.4 Lexical Error Handling

**Error Reporting:** Following Louden's recommendations (pp. 70-72), the lexer reports:
- Character position (line and column)
- Context of the error
- Unexpected character

**Example Error:**
```python
raise SyntaxError(
    f"Unexpected character '{current}' at line {self.line}, column {self.column}"
)
```

### 2.5 Token Data Structure

**Implementation:** (Louden Section 2.2, pp. 32-34)

```python
# src/lexer/token.py
@dataclass
class Token:
    type: TokenType      # Token category (keyword, identifier, etc.)
    value: Any           # Lexical value (string, number, etc.)
    line: int            # Line number (for error reporting)
    column: int          # Column number (for error reporting)
```

**Token Type Enumeration:**
```python
class TokenType(Enum):
    # Keywords (40+ types)
    VAR = auto()
    LOAD = auto()
    # ...
    
    # Literals
    REGISTER = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Operators
    EQ = auto()  # ==
    NEQ = auto()  # !=
    # ...
    
    # Special
    NEWLINE = auto()
    EOF = auto()
```

---

## 3. Syntax Definition (Grammar)

### 3.1 Grammar Notation and Parser Theory

Following **Louden Chapter 3** (Context-Free Grammars) and **Chapter 4** (Top-Down Parsing), our grammar is specified in **Extended Backus-Naur Form (EBNF)** and designed for **LL(1) recursive descent parsing**.

**Key Properties:**
- **LL(1) compatible**: One token lookahead sufficient (Louden Section 4.4, pp. 143-149)
- **No left recursion**: Required for recursive descent (Louden pp. 136-137)
- **Unambiguous**: Each construct has unique parse tree (Louden pp. 90-94)

### 3.2 Program Structure

```bnf
program ::= statement* EOF

statement ::= var_decl | data_op | arithmetic_op | bitwise_op | control_flow 
            | function_def | function_call | stack_op | io_op | special_op 
            | NEWLINE
```

**Parser Implementation:** (Louden Section 4.3, pp. 131-138 - Recursive Descent)

```python
# src/parser/parser.py - parse()
def parse(self):
    ast = []
    while self.current_token().type != TokenType.EOF:
        stmt = self.parse_statement()
        if stmt:
            ast.append(stmt)
        self.skip_newlines()
    
    return Program(ast)  # AST root node
```

**Dispatch Table Pattern:** (Louden pp. 138-140 - Table-driven parsing)
```python
# src/parser/parser.py - Statement handler mapping
self._statement_handlers = {
    TokenType.VAR: self.parse_var_decl,
    TokenType.LOAD: self.parse_load,
    TokenType.SET: self.parse_set,
    TokenType.PRINT: self.parse_print,
    # ... 40+ mappings
}
```

### 3.3 Variable Declarations

```bnf
var_decl ::= VAR identifier (',' number)? NEWLINE
```

**Semantics:**
- Declares a global variable with optional initialization
- If no initial value, variable is zero-initialized

**Examples:**
```assembly
VAR counter           ; Declares counter = 0
VAR sum, 100          ; Declares sum = 100
VAR flag, 0x1         ; Declares flag = 1 (hex)
```

**Parser Implementation:**
```python
# src/parser/parser.py - parse_var_decl()
def parse_var_decl(self) -> VarDecl:
    self.expect(TokenType.VAR)
    name = self.expect(TokenType.IDENTIFIER).value
    
    value = None
    if self.current_token().type == TokenType.COMMA:
        self.advance()
        value = self.expect(TokenType.NUMBER).value
    
    return VarDecl(name, value)
```

**AST Node:**
```python
# src/ast/node.py
@dataclass
class VarDecl(ASTNode):
    name: str                    # Variable identifier
    value: Optional[int] = None  # Initial value (or None)
```

**Code Generation:** (Louden Section 8.3, pp. 383-384 - Memory layout)
```python
# src/generator/nasm_generator.py - generate_var_decl()
def generate_var_decl(self, stmt: VarDecl):
    self.variables[stmt.name] = True
    if stmt.value is not None:
        self.emit_data(f"{stmt.name} dq {stmt.value}")  # .data section
    else:
        self.emit_bss(f"{stmt.name} resq 1")            # .bss section
```

**Generated Assembly:**
```nasm
section .data
    sum dq 100        ; Initialized variable

section .bss
    counter resq 1    ; Uninitialized variable
```

### 3.4 Data Movement Operations

#### 3.4.1 LOAD - Load Value into Register

```bnf
load_stmt ::= LOAD register ',' value NEWLINE
value     ::= register | identifier | number
```

**Semantics:** Loads a value (immediate, variable, or register) into a register.

**Examples:**
```assembly
LOAD R1, 42        ; R1 = 42 (immediate)
LOAD R2, counter   ; R2 = [counter] (memory)
LOAD R3, R1        ; R3 = R1 (register)
```

**Code Generation:**
```python
# src/generator/nasm_generator.py - generate_load()
def generate_load(self, stmt: Load):
    dest = self.get_register(stmt.dest)  # R1 -> rax
    
    if isinstance(stmt.src, int):
        self.emit(f"mov {dest}, {stmt.src}")      # Immediate
    elif self.is_register(stmt.src):
        self.emit(f"mov {dest}, {self.get_register(stmt.src)}")  # Register
    else:
        self.emit(f"mov {dest}, [{stmt.src}]")    # Memory
```

#### 3.4.2 SET - Store Value to Memory

```bnf
set_stmt ::= SET identifier ',' (register | number) NEWLINE
```

**Semantics:** Stores a register or immediate value to a variable in memory.

**Examples:**
```assembly
SET counter, R1    ; [counter] = R1
SET sum, 100       ; [sum] = 100
```

**Code Generation:**
```python
# src/generator/nasm_generator.py - generate_set()
def generate_set(self, stmt: Set):
    if isinstance(stmt.src, int):
        self.emit(f"mov qword [{stmt.dest}], {stmt.src}")
    else:
        self.emit(f"mov qword [{stmt.dest}], {self.get_register(stmt.src)}")
```

#### 3.4.3 MOVE - Copy Between Registers

```bnf
move_stmt ::= MOVE register ',' register NEWLINE
```

**Semantics:** Copies value from one register to another.

**Example:**
```assembly
MOVE R2, R1    ; R2 = R1
```

### 3.5 Arithmetic Operations

Following Louden Section 8.3 (pp. 380-388 - Basic Code Generation), arithmetic operations use **three-address code** format.

```bnf
arithmetic_op ::= (ADD | SUB | MUL | DIV) register ',' register ',' (register | number) NEWLINE
unary_op      ::= (INC | DEC) (register | identifier) NEWLINE
```

**Semantics:**
- Binary: `dest = left op right`
- Unary: `operand = operand op 1`

**Examples:**
```assembly
ADD R3, R1, R2     ; R3 = R1 + R2
SUB R2, R1, 10     ; R2 = R1 - 10
MUL R3, R2, R1     ; R3 = R2 * R1
DIV R1, R1, 2      ; R1 = R1 / 2
INC R1             ; R1 = R1 + 1
DEC counter        ; counter = counter - 1
```

**Special Case - Division:** (Louden pp. 390-392 - Register constraints)

DIV uses x86-64's `div` instruction which has implicit operands:
- **Input:** Dividend in RAX, Divisor in register/memory
- **Output:** Quotient in RAX, Remainder in RDX

**Code Generation:**
```python
# src/generator/nasm_generator.py - generate_binary_op() - DIV case
if stmt.op == "DIV":
    # Save registers that DIV clobbers
    if dest != "rdx":
        self.emit("push rdx")
    
    save_rax = dest != "rax"
    if save_rax:
        self.emit("push rax")
    
    # Move dividend to rax
    if left != "rax":
        self.emit(f"mov rax, {left}")
    
    self.emit("xor rdx, rdx")  # Clear rdx for unsigned division
    
    # Divide
    if isinstance(stmt.right, int):
        self.emit("push r10")
        self.emit(f"mov r10, {stmt.right}")
        self.emit("div r10")
        self.emit("pop r10")
    else:
        self.emit(f"div {right_operand}")
    
    # Move quotient to destination
    if dest != "rax":
        self.emit(f"mov {dest}, rax")
    
    # Restore saved registers
    if save_rax:
        self.emit("pop rax")
    if dest != "rdx":
        self.emit("pop rdx")
```

### 3.6 Bitwise Operations

```bnf
bitwise_op ::= binary_bitwise | unary_bitwise | shift_op

binary_bitwise ::= (AND | OR | XOR) register ',' register ',' (register | number) NEWLINE
unary_bitwise  ::= NOT register NEWLINE
shift_op       ::= (SHL | SHR) register ',' register ',' number NEWLINE
```

**Semantics:**
- AND, OR, XOR: `dest = left op right`
- NOT: Bitwise negation (`dest = ~dest`)
- SHL/SHR: Logical shift (`dest = src << count` or `dest = src >> count`)

**Examples:**
```assembly
AND R3, R1, R2     ; R3 = R1 & R2 (bitwise AND)
OR R3, R1, R2      ; R3 = R1 | R2 (bitwise OR)
XOR R3, R1, R2     ; R3 = R1 ^ R2 (bitwise XOR)
NOT R1             ; R1 = ~R1 (bitwise NOT)
SHL R2, R1, 2      ; R2 = R1 << 2 (shift left by 2)
SHR R2, R1, 3      ; R2 = R1 >> 3 (shift right by 3)
```

### 3.7 Control Flow Structures

Following Louden Section 8.5 (pp. 397-405 - Code Generation for Control Structures), control flow is implemented using **labels and conditional jumps**.

#### 3.7.1 IF Statement

```bnf
if_stmt ::= IF condition NEWLINE
            statement*
            (ELSE NEWLINE statement*)?
            ENDIF

condition ::= value compare_op value
compare_op ::= '==' | '!=' | '>' | '<' | '>=' | '<='
```

**Semantics:** Conditional execution with optional else branch.

**Examples:**
```assembly
IF R1 > 10
    LOAD R2, 1
ENDIF

IF counter == 0
    PRINT R1
ELSE
    PRINT R2
ENDIF
```

**Parser Implementation:** (Louden Section 4.3, pp. 135-138)
```python
# src/parser/parser.py - parse_if()
def parse_if(self) -> If:
    self.expect(TokenType.IF)
    condition = self.parse_condition()
    self.skip_newlines()
    
    # Parse then body
    then_body = []
    while self.current_token().type not in [TokenType.ELSE, TokenType.ENDIF]:
        stmt = self.parse_statement()
        if stmt:
            then_body.append(stmt)
        self.skip_newlines()
    
    # Parse optional else body
    else_body = None
    if self.current_token().type == TokenType.ELSE:
        self.advance()
        self.skip_newlines()
        else_body = self._parse_body(TokenType.ENDIF)
    
    self.expect(TokenType.ENDIF)
    return If(condition, then_body, else_body)
```

**Code Generation:** (Louden pp. 401-403 - Label generation for conditionals)
```python
# src/generator/nasm_generator.py - generate_if()
def generate_if(self, stmt: If):
    else_label = f"else_{self.label_counter}"
    endif_label = f"endif_{self.label_counter}"
    self.label_counter += 1
    
    # Evaluate condition and jump to else_label if false
    self.generate_condition(stmt.condition, else_label)
    
    # Generate then body
    for s in stmt.then_body:
        self.generate_statement(s)
    
    if stmt.else_body:
        self.emit(f"jmp {endif_label}")
        self.emit_label(else_label)
        for s in stmt.else_body:
            self.generate_statement(s)
        self.emit_label(endif_label)
    else:
        self.emit_label(else_label)
```

**Generated Assembly Example:**
```nasm
; IF R1 > 10
    mov r10, rax       ; Load R1 to temporary
    mov r11, 10        ; Load comparison value
    cmp r10, r11       ; Compare
    jle else_0         ; Jump if NOT greater

    ; Then body
    mov rax, 1         ; LOAD R2, 1
    
    jmp endif_0        ; Skip else

else_0:
    ; Else body (if present)

endif_0:
```

#### 3.7.2 WHILE Loop

```bnf
while_stmt ::= WHILE condition NEWLINE
               statement*
               ENDWHILE
```

**Semantics:** Pre-condition loop - executes while condition is true.

**Example:**
```assembly
WHILE counter > 0
    DEC counter
    PRINT counter
ENDWHILE
```

**Code Generation:** (Louden pp. 403-404 - While loop implementation)
```python
# src/generator/nasm_generator.py - generate_while()
def generate_while(self, stmt: While):
    start_label = f"while_start_{self.label_counter}"
    end_label = f"while_end_{self.label_counter}"
    self.label_counter += 1
    
    self.emit_label(start_label)
    
    # Evaluate condition, jump to end if false
    self.generate_condition(stmt.condition, end_label)
    
    # Loop body
    for s in stmt.body:
        self.generate_statement(s)
    
    self.emit(f"jmp {start_label}")  # Repeat
    self.emit_label(end_label)
```

**Generated Assembly:**
```nasm
while_start_0:
    mov r10, [counter]
    mov r11, 0
    cmp r10, r11
    jle while_end_0    ; Exit if counter <= 0
    
    ; Body
    dec qword [counter]
    ; ... print logic ...
    
    jmp while_start_0
while_end_0:
```

#### 3.7.3 FOR Loop

```bnf
for_stmt ::= FOR identifier FROM number TO number (STEP number)? NEWLINE
             statement*
             ENDFOR
```

**Semantics:** Range-based loop with optional step (default = 1).

**Examples:**
```assembly
FOR i FROM 1 TO 10
    PRINT i
ENDFOR

FOR i FROM 0 TO 100 STEP 5
    PRINT i
ENDFOR

FOR i FROM 10 TO 1 STEP -1   ; Descending
    PRINT i
ENDFOR
```

**Code Generation:**
```python
# src/generator/nasm_generator.py - generate_for()
def generate_for(self, stmt: For):
    # Declare variable if needed
    if stmt.var not in self.variables:
        self.variables[stmt.var] = True
        self.emit_bss(f"{stmt.var} resq 1")
    
    start_label = f"for_start_{self.label_counter}"
    end_label = f"for_end_{self.label_counter}"
    self.label_counter += 1
    
    # Initialize loop variable
    self.emit(f"mov qword [{stmt.var}], {stmt.start}")
    
    self.emit_label(start_label)
    
    # Check condition based on step direction
    self.emit(f"mov r10, [{stmt.var}]")
    self.emit(f"mov r11, {stmt.end}")
    self.emit("cmp r10, r11")
    if stmt.step > 0:
        self.emit(f"jg {end_label}")  # Exit if var > end
    else:
        self.emit(f"jl {end_label}")  # Exit if var < end
    
    # Body
    for s in stmt.body:
        self.generate_statement(s)
    
    # Increment by step
    if stmt.step == 1:
        self.emit(f"inc qword [{stmt.var}]")
    elif stmt.step == -1:
        self.emit(f"dec qword [{stmt.var}]")
    else:
        self.emit(f"add qword [{stmt.var}], {stmt.step}")
    
    self.emit(f"jmp {start_label}")
    self.emit_label(end_label)
```

#### 3.7.4 LOOP Statement

```bnf
loop_stmt ::= LOOP identifier ',' number NEWLINE
              statement*
              ENDLOOP
```

**Semantics:** Loop while `var < limit`. Variable must be declared beforehand.

**Example:**
```assembly
VAR i, 0
LOOP i, 10
    PRINT i
    INC i
ENDLOOP
```

#### 3.7.5 REPEAT-UNTIL Loop

```bnf
repeat_stmt ::= REPEAT NEWLINE
                statement*
                UNTIL condition
```

**Semantics:** Post-condition loop - executes at least once, repeats until condition is true.

**Example:**
```assembly
REPEAT
    INC x
    PRINT x
UNTIL x >= 5
```

**Code Generation:** (Louden pp. 404-405 - Post-test loops)
```python
# src/generator/nasm_generator.py - generate_repeat()
def generate_repeat(self, stmt: Repeat):
    start_label = f"repeat_start_{self.label_counter}"
    self.label_counter += 1
    
    self.emit_label(start_label)
    
    # Body (executes at least once)
    for s in stmt.body:
        self.generate_statement(s)
    
    # Check condition - if FALSE, jump back
    # Note: We invert the logic - jump back if condition is NOT met
    self.generate_condition(stmt.condition, start_label)
```

### 3.8 Functions

Following Louden Section 8.6 (pp. 407-412 - Code Generation for Functions).

```bnf
function_def  ::= FUNC identifier NEWLINE
                  statement*
                  ENDFUNC

function_call ::= CALL identifier

return_stmt   ::= RET (register)?
```

**Semantics:**
- Functions are global named code blocks
- No formal parameters (use registers or global variables)
- Return value conventionally in R1 (rax)
- `RET` without register returns without value

**Example:**
```assembly
FUNC add_numbers
    LOAD R1, a
    LOAD R2, b
    ADD R3, R1, R2
    RET R3
ENDFUNC

VAR a, 10
VAR b, 20
CALL add_numbers
PRINT R1    ; Prints 30
```

**Code Generation:**
```python
# src/generator/nasm_generator.py - generate_function()
def generate_function(self, stmt: Function):
    self.emit_label(f"{stmt.name}")
    for s in stmt.body:
        self.generate_statement(s)

def generate_call(self, stmt: Call):
    self.emit(f"call {stmt.name}")

def generate_return(self, stmt: Return):
    if stmt.value:
        if self.is_register(stmt.value):
            self.emit(f"mov rax, {self.get_register(stmt.value)}")
    self.emit("ret")
```

### 3.9 Stack Operations

```bnf
stack_op ::= PUSH register | POP register
```

**Semantics:**
- PUSH: Save register value to stack
- POP: Restore register value from stack
- Follows x86-64 stack conventions (grows downward)

**Example:**
```assembly
PUSH R1              ; Save R1
CALL risky_function  ; Function may clobber R1
POP R1               ; Restore R1
```

### 3.10 Input/Output Operations

```bnf
io_op ::= print_stmt | input_stmt

print_stmt ::= PRINT value NEWLINE
input_stmt ::= INPUT (register | identifier) NEWLINE
```

**PRINT:** Output integer value to stdout (followed by newline).

**INPUT:** Read integer from stdin.

**Examples:**
```assembly
PRINT R1             ; Print register
PRINT counter        ; Print variable
PRINT 42             ; Print literal

INPUT R1             ; Read into register
INPUT user_value     ; Read into variable
```

**Implementation Note:** (Louden pp. 415-420 - I/O and Runtime Support)

PRINT and INPUT are implemented as **helper functions** that use Linux syscalls:
- `sys_write` (syscall 1) for output
- `sys_read` (syscall 0) for input

```python
# src/generator/nasm_generator.py - generate_print()
def generate_print(self, stmt: Print):
    self.needs_print_int = True  # Flag to include helper function
    
    # Load value to r15 (scratch register)
    self._load_value_to_r15(stmt.value)
    self.emit("call print_int")  # Call helper
```

The `print_int` helper function (Louden pp. 417-418):
1. Converts integer to decimal string
2. Writes string to stdout using syscall
3. Preserves user registers R1-R8

### 3.11 Special Operations

```bnf
special_op ::= HALT | NOP
```

**HALT:** Terminate program execution (exit with code 0).
**NOP:** No operation (placeholder).

**Examples:**
```assembly
HALT    ; Exit program
NOP     ; Do nothing (can be used for alignment or debugging)
```

---

## 4. Semantic Analysis

Following **Louden Chapter 6** (Semantic Analysis), our compiler performs semantic checks during parsing and code generation.

### 4.1 Symbol Table (Louden Section 6.2, pp. 253-262)

**Implementation:**
```python
# src/generator/nasm_generator.py
class NasmGenerator:
    def __init__(self):
        self.variables = {}  # Symbol table: {name: True}
        self.functions = []  # Function list
```

**Symbol Table Operations:**
- **Insert:** Add variable/function name
- **Lookup:** Check if name is declared
- **Scope:** All symbols are global

### 4.2 Type System (Louden Section 6.3, pp. 263-271)

TinyCompiled has a **simplified type system**:
- **Single type:** 64-bit signed integer (qword)
- **No type checking:** All operations assume integer operands
- **No implicit conversions:** (none needed)

### 4.3 Semantic Rules

#### 4.3.1 Variable Declaration

**Rule:** Variables must be declared with `VAR` before use in `SET` or `INPUT`.

**Note:** `LOAD` can read from undeclared variables (generates assembly error at link time if variable doesn't exist).

#### 4.3.2 Register Usage

**Rule:** Only R1-R8 are valid register names.

**Enforcement:** Lexer recognizes only these patterns.

#### 4.3.3 Function Definitions

**Rule:** Function names must be unique.

**Rule:** Functions can call other functions (including recursion).

#### 4.3.4 Control Flow Nesting

**Rule:** All control structures must be properly closed:
- `IF` ... `ENDIF`
- `WHILE` ... `ENDWHILE`
- `FOR` ... `ENDFOR`
- `LOOP` ... `ENDLOOP`
- `REPEAT` ... `UNTIL`
- `FUNC` ... `ENDFUNC`

**Enforcement:** Parser grammar ensures proper nesting through `_parse_body()` helper.

### 4.4 Error Handling (Louden Section 2.4, pp. 70-72)

**Lexical Errors:**
```python
raise SyntaxError(f"Unexpected character '{current}' at line {self.line}, column {self.column}")
```

**Syntax Errors:**
```python
def expect(self, expected: TokenType):
    token = self.current_token()
    if token.type != expected:
        raise SyntaxError(
            f"Expected token {expected}, but got {token.type} at line {token.line}, column {token.column}"
        )
```

---

## 5. Code Generation

Following **Louden Chapter 8** (Code Generation), our code generator produces x86-64 NASM assembly.

### 5.1 Target Architecture

**Platform:** x86-64 Linux  
**Assembler:** NASM (Netwide Assembler)  
**ABI:** System V AMD64 calling convention (for syscalls only)

### 5.2 Register Allocation (Louden Section 8.4, pp. 389-396)

**Strategy:** Direct mapping (no register allocation algorithm needed).

Each virtual register R1-R8 maps to a fixed physical register:

```python
# src/generator/nasm_generator.py
REGISTER_MAP = {
    "R1": "rax",   # Accumulator
    "R2": "rbx",   # Base
    "R3": "rcx",   # Counter
    "R4": "rdx",   # Data
    "R5": "rsi",   # Source index
    "R6": "rdi",   # Destination index
    "R7": "r8",    # General purpose
    "R8": "r9",    # General purpose
}
```

**Scratch Registers:** r10-r15 used for temporaries in generated code.

### 5.3 Memory Layout (Louden Section 8.3, pp. 383-384)

**Assembly Structure:**
```nasm
section .data       ; Initialized variables
    var1 dq 100

section .bss        ; Uninitialized variables
    var2 resq 1

section .text       ; Code
    global _start
_start:
    ; Program code
```

### 5.4 Code Generation Strategy (Louden pp. 380-388)

**Template-Based Generation:** Each AST node type has a corresponding code generation method.

**Example - Load Instruction:**
```python
def generate_load(self, stmt: Load):
    dest = self.get_register(stmt.dest)  # Virtual -> Physical
    
    if isinstance(stmt.src, int):
        self.emit(f"mov {dest}, {stmt.src}")          # Immediate
    elif self.is_register(stmt.src):
        src_reg = self.get_register(stmt.src)
        self.emit(f"mov {dest}, {src_reg}")           # Register
    else:
        self.emit(f"mov {dest}, [{stmt.src}]")        # Memory
```

**Generated Code Patterns:**
```nasm
; LOAD R1, 42
mov rax, 42

; LOAD R1, counter
mov rax, [counter]

; LOAD R1, R2
mov rax, rbx
```

### 5.5 Runtime Support (Louden pp. 415-420)

**Helper Functions:** For I/O operations, we generate helper functions:

**1. print_int** - Converts integer to string and writes to stdout
```nasm
print_int:
    ; Save caller's registers
    push rax
    push rbx
    ; ... (convert r15 to string) ...
    ; syscall write
    ; Restore registers
    pop rbx
    pop rax
    ret
```

**2. read_int** - Reads string from stdin and converts to integer
```nasm
read_int:
    ; syscall read
    ; ... (parse string to integer in r15) ...
    ret
```

### 5.6 Condition Code Generation (Louden pp. 397-401)

**Strategy:** Load operands to temporaries, compare, conditional jump.

```python
def generate_condition(self, cond: Condition, false_label: str):
    # Load left operand to r10
    if isinstance(cond.left, int):
        self.emit(f"mov r10, {cond.left}")
    elif self.is_register(cond.left):
        self.emit(f"mov r10, {self.get_register(cond.left)}")
    else:
        self.emit(f"mov r10, [{cond.left}]")
    
    # Load right operand to r11
    # ... (similar) ...
    
    # Compare and jump if condition is FALSE
    self.emit("cmp r10, r11")
    
    if cond.op == "==":
        self.emit(f"jne {false_label}")  # Jump if NOT equal
    elif cond.op == "!=":
        self.emit(f"je {false_label}")   # Jump if equal
    elif cond.op == ">":
        self.emit(f"jle {false_label}")  # Jump if less or equal
    # ... etc
```

### 5.7 Label Generation (Louden pp. 402-403)

**Strategy:** Unique labels using counter.

```python
class NasmGenerator:
    def __init__(self):
        self.label_counter = 0
    
    def generate_if(self, stmt: If):
        else_label = f"else_{self.label_counter}"
        endif_label = f"endif_{self.label_counter}"
        self.label_counter += 1
        # ...
```

**Generated Labels:**
```nasm
if_0:
else_0:
endif_0:
while_start_1:
while_end_1:
for_start_2:
for_end_2:
```

---

## 6. Complete Example with Generated Code

### 6.1 Source Code (Fibonacci)

```assembly
; Fibonacci function
FUNC fibonacci
    IF n == 0
        LOAD R1, 0
        RET R1
    ENDIF
    
    IF n == 1
        LOAD R1, 1
        RET R1
    ENDIF
    
    VAR a, 0
    VAR b, 1
    VAR i, 2
    
    WHILE i <= n
        LOAD R1, a
        LOAD R2, b
        ADD R3, R1, R2
        SET a, R2
        SET b, R3
        INC i
    ENDWHILE
    
    LOAD R1, b
    RET R1
ENDFUNC

VAR n, 10
CALL fibonacci
PRINT R1
HALT
```

### 6.2 Generated NASM Assembly (Excerpt)

```nasm
section .data
    n dq 10
    a dq 0
    b dq 1
    i dq 2
    newline db 10
    digit_buffer times 20 db 0

section .bss

section .text
    global _start

_start:
    jmp main_code

main_code:
    call fibonacci
    mov r15, rax
    call print_int
    mov rax, 60
    mov rdi, 0
    syscall

fibonacci:
    ; IF n == 0
    mov r10, [n]
    mov r11, 0
    cmp r10, r11
    jne else_0
    mov rax, 0
    ret
else_0:
    
    ; IF n == 1
    mov r10, [n]
    mov r11, 1
    cmp r10, r11
    jne else_1
    mov rax, 1
    ret
else_1:
    
    ; WHILE i <= n
while_start_2:
    mov r10, [i]
    mov r11, [n]
    cmp r10, r11
    jg while_end_2
    
    mov rax, [a]      ; LOAD R1, a
    mov rbx, [b]      ; LOAD R2, b
    mov rcx, rax      ; ADD R3, R1, R2
    add rcx, rbx
    mov qword [a], rbx    ; SET a, R2
    mov qword [b], rcx    ; SET b, R3
    inc qword [i]         ; INC i
    
    jmp while_start_2
while_end_2:
    
    mov rax, [b]      ; LOAD R1, b
    ret

print_int:
    ; (Helper function implementation)
    ; ...
```

---

## 7. Compiler Implementation Methodology

Following **Louden Chapter 1.4** (pp. 12-18 - Compiler Structure), we implemented the compiler in phases:

### 7.1 Phase 1: Lexical Analyzer
- **Input:** Source code string
- **Output:** Token stream
- **File:** `src/lexer/lexer.py`
- **Theory:** Louden Chapter 2 (Scanning)

### 7.2 Phase 2: Parser
- **Input:** Token stream
- **Output:** Abstract Syntax Tree (AST)
- **File:** `src/parser/parser.py`
- **Theory:** Louden Chapters 3-4 (Grammars and Parsing)

### 7.3 Phase 3: Code Generator
- **Input:** AST
- **Output:** NASM assembly code
- **File:** `src/generator/nasm_generator.py`
- **Theory:** Louden Chapter 8 (Code Generation)

### 7.4 Integration
- **File:** `src/compiler/compiler.py`
- **Pipeline:** Source → Lexer → Parser → Generator → Assembly

```python
def compile_tc_to_nasm(source_code: str) -> str:
    # Phase 1: Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Phase 2: Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Phase 3: Code Generation
    generator = NasmGenerator()
    asm_code = generator.generate(ast)
    
    return asm_code
```

---

## 8. References and Theoretical Foundations

### 8.1 Primary Reference

**Louden, Kenneth C.** (1997). *Compiler Construction: Principles and Practice*. PWS Publishing Company. ISBN 0-534-93972-4.

**Chapters Applied:**
- **Chapter 1** (pp. 1-28): Compiler structure and overview
- **Chapter 2** (pp. 29-80): Lexical analysis and scanning
- **Chapter 3** (pp. 81-130): Context-free grammars and syntax
- **Chapter 4** (pp. 131-172): Top-down parsing (recursive descent)
- **Chapter 6** (pp. 249-302): Semantic analysis and symbol tables
- **Chapter 8** (pp. 361-420): Code generation for assembly

### 8.2 Additional References

**Aho, A. V., Sethi, R., & Ullman, J. D.** (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.

**Appel, A. W.** (2004). *Modern Compiler Implementation in C*. Cambridge University Press.

**Intel Corporation** (2023). *Intel® 64 and IA-32 Architectures Software Developer's Manual*.

**System V Application Binary Interface** - AMD64 Architecture Processor Supplement.

---

## 9. Appendix A: Complete Grammar (BNF)

```bnf
program        ::= statement* EOF

statement      ::= var_decl | load_stmt | set_stmt | move_stmt
                 | arithmetic_op | bitwise_op | shift_op | unary_op
                 | if_stmt | while_stmt | for_stmt | loop_stmt | repeat_stmt
                 | function_def | function_call | return_stmt
                 | push_stmt | pop_stmt
                 | print_stmt | input_stmt
                 | halt_stmt | nop_stmt
                 | NEWLINE

var_decl       ::= VAR identifier (',' number)? NEWLINE

load_stmt      ::= LOAD register ',' value NEWLINE
set_stmt       ::= SET identifier ',' (register | number) NEWLINE
move_stmt      ::= MOVE register ',' register NEWLINE

arithmetic_op  ::= (ADD | SUB | MUL | DIV) register ',' register ',' value NEWLINE
unary_op       ::= (INC | DEC) (register | identifier) NEWLINE

bitwise_op     ::= (AND | OR | XOR) register ',' register ',' value NEWLINE
                 | NOT register NEWLINE
shift_op       ::= (SHL | SHR) register ',' register ',' number NEWLINE

if_stmt        ::= IF condition NEWLINE statement* (ELSE NEWLINE statement*)? ENDIF
while_stmt     ::= WHILE condition NEWLINE statement* ENDWHILE
for_stmt       ::= FOR identifier FROM number TO number (STEP number)? NEWLINE statement* ENDFOR
loop_stmt      ::= LOOP identifier ',' number NEWLINE statement* ENDLOOP
repeat_stmt    ::= REPEAT NEWLINE statement* UNTIL condition

function_def   ::= FUNC identifier NEWLINE statement* ENDFUNC
function_call  ::= CALL identifier NEWLINE
return_stmt    ::= RET (register)? NEWLINE

push_stmt      ::= PUSH register NEWLINE
pop_stmt       ::= POP register NEWLINE

print_stmt     ::= PRINT value NEWLINE
input_stmt     ::= INPUT (register | identifier) NEWLINE

halt_stmt      ::= HALT NEWLINE
nop_stmt       ::= NOP NEWLINE

condition      ::= value compare_op value
compare_op     ::= '==' | '!=' | '>' | '<' | '>=' | '<='

value          ::= register | identifier | number

register       ::= 'R1' | 'R2' | 'R3' | 'R4' | 'R5' | 'R6' | 'R7' | 'R8'
identifier     ::= (letter | '_') (letter | digit | '_')*
number         ::= decimal | hexadecimal | binary

decimal        ::= '-'? digit+
hexadecimal    ::= '-'? '0' ('x' | 'X') hexdigit+
binary         ::= '-'? '0' ('b' | 'B') ('0' | '1')+

letter         ::= 'a'..'z' | 'A'..'Z'
digit          ::= '0'..'9'
hexdigit       ::= digit | 'a'..'f' | 'A'..'F'
```

---

## 10. Appendix B: Token Type Summary

| Category | Token Types |
|----------|------------|
| **Data Movement** | VAR, LOAD, SET, MOVE |
| **Arithmetic** | ADD, SUB, MUL, DIV, INC, DEC |
| **Bitwise** | AND, OR, XOR, NOT, SHL, SHR |
| **Control Flow** | IF, ELSE, ENDIF, WHILE, ENDWHILE, FOR, ENDFOR, FROM, TO, STEP, LOOP, ENDLOOP, REPEAT, UNTIL |
| **Functions** | FUNC, ENDFUNC, CALL, RET |
| **Stack** | PUSH, POP |
| **I/O** | PRINT, INPUT |
| **Special** | HALT, NOP |
| **Literals** | REGISTER, IDENTIFIER, NUMBER |
| **Operators** | EQ, NEQ, GT, LT, GTE, LTE |
| **Punctuation** | COMMA, COLON, NEWLINE, EOF |

---

## 11. Appendix C: AST Node Types

```python
# Complete AST node hierarchy
Program         # Root node containing statement list
VarDecl         # Variable declaration
Load            # Load to register
Set             # Store to memory
Move            # Register-to-register move
BinaryOp        # ADD, SUB, MUL, DIV, AND, OR, XOR
UnaryOp         # INC, DEC, NOT
ShiftOp         # SHL, SHR
Function        # Function definition
Call            # Function call
Return          # Return statement
Loop            # LOOP statement
While           # WHILE loop
For             # FOR loop
Repeat          # REPEAT-UNTIL loop
If              # IF-ELSE-ENDIF
Condition       # Comparison expression
Push            # Stack push
Pop             # Stack pop
Print           # Output operation
Input           # Input operation
Halt            # Program termination
Nop             # No operation
```

---

**End of Formal Definition**

This document serves as both a language specification and documentation of compiler implementation principles learned through hands-on development following Kenneth C. Louden's compiler construction methodology.

