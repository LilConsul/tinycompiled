# TinyCompiled Language Formal Definition

## 1. Introduction

TinyCompiled is a low-level assembly-like programming language that compiles to x86-64 NASM assembly. It provides a simple, instruction-based syntax with support for variables, registers, functions, control flow, and basic I/O operations.

## 2. Lexical Structure

### 2.1 Character Set

TinyCompiled source code is written in ASCII or UTF-8 encoding.

### 2.2 Tokens

The language consists of the following token types:

#### 2.2.1 Keywords (Case-Insensitive)

```
VAR LOAD SET MOVE
ADD SUB MUL DIV
INC DEC
AND OR XOR NOT
SHL SHR
FUNC ENDFUNC CALL RET
LOOP ENDLOOP WHILE ENDWHILE FOR ENDFOR FROM TO STEP
REPEAT UNTIL
IF ELSE ENDIF
PUSH POP
PRINT INPUT
HALT NOP
```

#### 2.2.2 Registers

Eight general-purpose registers (case-sensitive):
```
R1 R2 R3 R4 R5 R6 R7 R8
```

#### 2.2.3 Identifiers

An identifier is a sequence of characters used to name variables and functions.

**Syntax:**
```
identifier ::= (letter | '_') (letter | digit | '_')*
letter     ::= 'a'..'z' | 'A'..'Z'
digit      ::= '0'..'9'
```

**Rules:**
- Must start with a letter or underscore
- May contain letters, digits, and underscores
- Case-sensitive
- Cannot be a keyword or register name
- Examples: `counter`, `sum_total`, `my_var`, `_temp`

#### 2.2.4 Number Literals

**Decimal:**
```
decimal ::= '-'? digit+
```
Example: `42`, `-10`, `0`

**Hexadecimal:**
```
hexadecimal ::= '-'? '0' ('x' | 'X') hexdigit+
hexdigit    ::= digit | 'a'..'f' | 'A'..'F'
```
Example: `0xFF`, `0x2A`, `-0x10`

**Binary:**
```
binary ::= '-'? '0' ('b' | 'B') ('0' | '1')+
```
Example: `0b1010`, `0b11111111`

#### 2.2.5 Comparison Operators

```
==    Equal to
!=    Not equal to
>     Greater than
<     Less than
>=    Greater than or equal to
<=    Less than or equal to
```

#### 2.2.6 Punctuation

```
,     Comma (separator)
:     Colon (label marker, currently not used)
```

#### 2.2.7 Whitespace

Spaces and tabs are ignored except as token separators.

#### 2.2.8 Newlines

Newlines (`\n`) are significant and act as statement terminators.

#### 2.2.9 Comments

Single-line comments begin with `;` and continue to the end of the line.

```
; This is a comment
VAR x, 10  ; This is also a comment
```

## 3. Grammar

### 3.1 Program Structure

```bnf
program ::= statement*

statement ::= var_decl
            | data_movement
            | arithmetic_op
            | bitwise_op
            | control_flow
            | function_def
            | function_call
            | stack_op
            | io_op
            | special_op
            | NEWLINE
```

### 3.2 Variable Declaration

```bnf
var_decl ::= VAR identifier
           | VAR identifier ',' number

number ::= decimal | hexadecimal | binary
```

**Semantics:**
- Declares a variable with the given identifier
- If no initial value is provided, defaults to 0
- Variables are stored in the `.bss` or `.data` section

**Examples:**
```
VAR counter          ; counter = 0
VAR sum, 100         ; sum = 100
VAR max, 0xFF        ; max = 255
```

### 3.3 Data Movement

```bnf
data_movement ::= load_stmt | set_stmt | move_stmt

load_stmt ::= LOAD register ',' value
set_stmt  ::= SET identifier ',' reg_or_num
move_stmt ::= MOVE register ',' register

value      ::= register | identifier | number
reg_or_num ::= register | number
```

**Semantics:**
- `LOAD`: Loads a value into a register
- `SET`: Stores a value into a variable
- `MOVE`: Copies value from one register to another

**Examples:**
```
LOAD R1, 42          ; R1 = 42
LOAD R2, counter     ; R2 = counter
SET result, 10       ; result = 10
SET sum, R3          ; sum = R3
MOVE R2, R1          ; R2 = R1
```

### 3.4 Arithmetic Operations

```bnf
arithmetic_op ::= binary_arith | unary_arith

binary_arith ::= (ADD | SUB | MUL | DIV) register ',' register ',' reg_or_num
unary_arith  ::= (INC | DEC) (register | identifier)
```

**Semantics:**
- Binary operations: `dest = left op right`
- `INC`: Increment by 1
- `DEC`: Decrement by 1

**Examples:**
```
ADD R3, R1, R2       ; R3 = R1 + R2
ADD R1, R1, 5        ; R1 = R1 + 5
SUB R2, R1, 10       ; R2 = R1 - 10
MUL R3, R2, R1       ; R3 = R2 * R1
DIV R1, R1, 2        ; R1 = R1 / 2
INC R1               ; R1++
DEC counter          ; counter--
```

### 3.5 Bitwise Operations

```bnf
bitwise_op ::= binary_bitwise | unary_bitwise | shift_op

binary_bitwise ::= (AND | OR | XOR) register ',' register ',' register
unary_bitwise  ::= NOT register
shift_op       ::= (SHL | SHR) register ',' register ',' number
```

**Semantics:**
- Binary bitwise: `dest = left op right`
- `NOT`: Bitwise negation
- `SHL`: Shift left (logical)
- `SHR`: Shift right (logical)

**Examples:**
```
AND R3, R1, R2       ; R3 = R1 & R2
OR R3, R1, R2        ; R3 = R1 | R2
XOR R3, R1, R2       ; R3 = R1 ^ R2
NOT R1               ; R1 = ~R1
SHL R2, R1, 2        ; R2 = R1 << 2
SHR R2, R1, 3        ; R2 = R1 >> 3
```

### 3.6 Control Flow

```bnf
control_flow ::= if_stmt | loop_stmt | while_stmt | for_stmt | repeat_stmt

if_stmt ::= IF condition NEWLINE
            statement*
            (ELSE NEWLINE statement*)?
            ENDIF

loop_stmt ::= LOOP identifier ',' number NEWLINE
              statement*
              ENDLOOP

while_stmt ::= WHILE condition NEWLINE
               statement*
               ENDWHILE

for_stmt ::= FOR identifier FROM number TO number (STEP number)? NEWLINE
             statement*
             ENDFOR

repeat_stmt ::= REPEAT NEWLINE
                statement*
                UNTIL condition

condition ::= value compare_op value
compare_op ::= '==' | '!=' | '>' | '<' | '>=' | '<='
```

**Semantics:**
- `IF`: Conditional execution with optional else branch
- `LOOP`: Iterate while variable < limit (variable must exist)
- `WHILE`: Pre-condition loop
- `FOR`: Range-based loop with optional step (default step = 1)
- `REPEAT`: Post-condition loop (executes at least once)

**Examples:**
```
IF R1 > 10
    LOAD R2, 1
ENDIF

IF counter == 0
    PRINT R1
ELSE
    PRINT R2
ENDIF

LOOP i, 10
    PRINT i
    INC i
ENDLOOP

WHILE counter > 0
    DEC counter
ENDWHILE

FOR i FROM 1 TO 10
    PRINT i
ENDFOR

FOR i FROM 0 TO 100 STEP 5
    PRINT i
ENDFOR

REPEAT
    INC x
UNTIL x >= 5
```

### 3.7 Functions

```bnf
function_def  ::= FUNC identifier NEWLINE
                  statement*
                  ENDFUNC

function_call ::= CALL identifier

return_stmt   ::= RET
                | RET register
```

**Semantics:**
- Functions are named blocks of code
- Functions can be called by name
- Return value is passed through a register (typically R1)
- `RET` without register returns without value
- `RET register` returns the value in the specified register

**Examples:**
```
FUNC add_numbers
    ADD R1, R1, R2
    RET R1
ENDFUNC

CALL add_numbers
PRINT R1
```

### 3.8 Stack Operations

```bnf
stack_op ::= PUSH register
           | POP register
```

**Semantics:**
- `PUSH`: Push register value onto the stack
- `POP`: Pop value from stack into register

**Examples:**
```
PUSH R1              ; Save R1 to stack
CALL my_function
POP R1               ; Restore R1 from stack
```

### 3.9 I/O Operations

```bnf
io_op ::= print_stmt | input_stmt

print_stmt ::= PRINT value
input_stmt ::= INPUT (register | identifier)
```

**Semantics:**
- `PRINT`: Output value to stdout (followed by newline)
- `INPUT`: Read integer from stdin

**Examples:**
```
PRINT R1             ; Print R1
PRINT counter        ; Print counter variable
PRINT 42             ; Print literal 42
INPUT R1             ; Read input into R1
INPUT user_value     ; Read input into user_value
```

### 3.10 Special Operations

```bnf
special_op ::= HALT | NOP
```

**Semantics:**
- `HALT`: Terminate program execution (exit with code 0)
- `NOP`: No operation (placeholder)

**Examples:**
```
HALT                 ; Exit program
NOP                  ; Do nothing
```

## 4. Semantic Rules

### 4.1 Registers

- Eight general-purpose registers: R1-R8
- Mapped to x86-64 registers: R1→rax, R2→rbx, R3→rcx, R4→rdx, R5→rsi, R6→rdi, R7→r8, R8→r9
- Registers are not preserved across function calls (caller-saved)

### 4.2 Variables

- Variables must be declared with `VAR` before use
- Variables are 64-bit signed integers (quadword)
- Variables are global in scope
- Variable names are case-sensitive

### 4.3 Functions

- Functions are defined with `FUNC name` ... `ENDFUNC`
- Functions can be called with `CALL name`
- No formal parameter passing mechanism (use registers or global variables)
- Return values conventionally passed in R1
- Functions can call other functions

### 4.4 Scoping

- All variables are global
- Function names must be unique
- No local variables within functions

### 4.5 Control Flow

- All control structures must be properly closed:
  - `IF` ... `ENDIF`
  - `WHILE` ... `ENDWHILE`
  - `LOOP` ... `ENDLOOP`
  - `FOR` ... `ENDFOR`
  - `REPEAT` ... `UNTIL`
  - `FUNC` ... `ENDFUNC`
- Nesting of control structures is allowed
- No explicit goto or jump instructions (use functions and loops instead)

### 4.6 Type System

- TinyCompiled is untyped at the language level
- All values are 64-bit signed integers
- No floating-point support
- No string support (except in PRINT for literals)

### 4.7 Evaluation Order

- Statements are executed sequentially
- Conditions are evaluated when encountered
- Loop conditions are checked at appropriate times (pre-condition for WHILE/FOR, post-condition for REPEAT)

### 4.8 Division by Zero

- Division by zero behavior is undefined
- Implementation may crash or produce unexpected results

## 5. Compilation Model

### 5.1 Target Platform

TinyCompiled compiles to x86-64 NASM assembly for Linux.

### 5.2 System Calls

- Uses Linux syscalls for I/O operations
- `sys_read` (syscall 0) for input
- `sys_write` (syscall 1) for output
- `sys_exit` (syscall 60) for program termination

### 5.3 Memory Layout

- `.bss` section: Uninitialized variables (VAR without initial value)
- `.data` section: Initialized variables and string constants
- `.text` section: Code (instructions)

### 5.4 ABI Compliance

- Does not follow System V AMD64 ABI for function calls
- Custom calling convention using global registers
- Stack operations (PUSH/POP) use the system stack

## 6. Examples

### 6.1 Hello World (Print a Number)

```
VAR message, 42
PRINT message
HALT
```

### 6.2 Factorial Function

```
VAR n, 5
VAR result, 1
VAR i, 1

LOOP i, 6
    LOAD R1, result
    LOAD R2, i
    MUL R3, R1, R2
    SET result, R3
    INC i
ENDLOOP

PRINT result
HALT
```

### 6.3 Fibonacci (Iterative)

```
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

## 7. Error Handling

### 7.1 Lexical Errors

- Invalid characters
- Malformed number literals
- Unterminated comments (not applicable, comments are single-line)

### 7.2 Syntax Errors

- Missing commas, keywords, or operands
- Mismatched control structure delimiters
- Invalid token sequences

### 7.3 Semantic Errors

- Use of undeclared variables
- Use of undeclared functions
- Invalid register names
- Type mismatches (wrong operand type for instruction)

### 7.4 Runtime Errors

- Division by zero
- Stack overflow/underflow
- Invalid memory access
- Integer overflow (wraps around, no error)

## 8. Reserved Words

The following keywords are reserved and cannot be used as identifiers:

```
VAR LOAD SET MOVE
ADD SUB MUL DIV INC DEC
AND OR XOR NOT SHL SHR
FUNC ENDFUNC CALL RET
LOOP ENDLOOP WHILE ENDWHILE FOR ENDFOR FROM TO STEP
REPEAT UNTIL
IF ELSE ENDIF
PUSH POP
PRINT INPUT
HALT NOP
```

## 9. Limits

- **Registers:** 8 (R1-R8)
- **Integer size:** 64-bit signed (-2^63 to 2^63-1)
- **Identifiers:** Unlimited length (implementation-dependent)
- **Nesting depth:** Unlimited (implementation-dependent)
- **Number of variables:** Unlimited (memory-dependent)
- **Number of functions:** Unlimited (memory-dependent)