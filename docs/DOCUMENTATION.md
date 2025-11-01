# TinyCompiled Instruction Set - Implementation Checklist

## Terminology

### `register`

A temporary storage location in the CPU for fast data access. TinyCompiled provides 8 registers: **R1, R2, R3, R4, R5,
R6, R7, R8**

Example: `R1`, `R5`, `R8`

### `identifier`

A user-defined name for a variable or function. Must start with a letter or underscore, can contain letters, digits, and
underscores.

Example: `counter`, `sum_total`, `my_var`, `_temp`

### `immediate`

A constant literal value embedded directly in the instruction. Can be decimal, hexadecimal, or binary.

Example: `42`, `-10`, `0xFF`, `0b1010`

### `condition`

A comparison expression used in control flow statements.

Example: `R1 > 10`, `counter == 0`, `x >= 5`

---

## 1. Variable Declaration

- [x] `VAR identifier` - Declare variable (default 0)
- [x] `VAR identifier, immediate` - Declare and initialize variable

**Examples:**

```tc
VAR counter          ; counter = 0
VAR sum, 100        ; sum = 100
```

---

## 2. Data Movement

- [x] `LOAD register, immediate` - Load immediate value into register
- [x] `LOAD register, identifier` - Load variable into register
- [x] `SET identifier, immediate` - Store immediate to variable
- [x] `SET identifier, register` - Store register to variable
- [x] `MOVE register, register` - Copy between registers

**Examples:**

```tc
LOAD R1, 42         ; R1 = 42
LOAD R2, counter    ; R2 = counter
SET result, 10      ; result = 10
SET sum, R3         ; sum = R3
MOVE R2, R1         ; R2 = R1
```

---

## 3. Arithmetic Operations

- [x] `ADD register, register, register` - Addition (dest = src1 + src2)
- [x] `ADD register, register, immediate` - Addition (dest = src + immediate)
- [x] `SUB register, register, register` - Subtraction (dest = src1 - src2)
- [x] `SUB register, register, immediate` - Subtraction (dest = src - immediate)
- [x] `MUL register, register, register` - Multiplication (dest = src1 * src2)
- [x] `MUL register, register, immediate` - Multiplication (dest = src * immediate)
- [x] `DIV register, register, register` - Division (dest = src1 / src2)
- [x] `DIV register, register, immediate` - Division (dest = src / immediate)
- [x] `INC register` - Increment register by 1
- [x] `INC identifier` - Increment variable by 1
- [x] `DEC register` - Decrement register by 1
- [x] `DEC identifier` - Decrement variable by 1

**Examples:**

```tc
ADD R3, R1, R2      ; R3 = R1 + R2
ADD R1, R1, 5       ; R1 = R1 + 5
SUB R2, R1, 10      ; R2 = R1 - 10
MUL R3, R2, R1      ; R3 = R2 * R1
DIV R1, R1, 2       ; R1 = R1 / 2
INC R1              ; R1++
DEC counter         ; counter--
```

---

## 4. Logical/Bitwise Operations

- [x] `AND register, register, register` - Bitwise AND (dest = src1 & src2)
- [x] `OR register, register, register` - Bitwise OR (dest = src1 | src2)
- [x] `XOR register, register, register` - Bitwise XOR (dest = src1 ^ src2)
- [x] `NOT register` - Bitwise NOT (register = ~register)
- [x] `SHL register, register, immediate` - Shift left (dest = src << count)
- [x] `SHR register, register, immediate` - Shift right (dest = src >> count)

**Examples:**

```tc
AND R3, R1, R2      ; R3 = R1 & R2
OR R3, R1, R2       ; R3 = R1 | R2
XOR R3, R1, R2      ; R3 = R1 ^ R2
NOT R1              ; R1 = ~R1
SHL R2, R1, 2       ; R2 = R1 << 2
SHR R2, R1, 3       ; R2 = R1 >> 3
```

---

## 5. Functions

- [x] `FUNC identifier` / `ENDFUNC` - Function definition
- [x] `CALL identifier` - Call function by name
- [x] `RET` - Return from function
- [x] `RET register` - Return with value in register

**Examples:**

```tc
FUNC add_numbers
    ADD R1, R1, R2
    RET R1
ENDFUNC

CALL add_numbers
```

---

## 6. Loop Constructs

- [x] `LOOP identifier, immediate` / `ENDLOOP` - Loop while var < limit
- [x] `WHILE condition` / `ENDWHILE` - Loop while condition is true
- [x] `FOR identifier FROM immediate TO immediate` / `ENDFOR` - Range loop
- [x] `FOR identifier FROM immediate TO immediate STEP immediate` / `ENDFOR` - Range loop with step
- [x] `REPEAT` / `UNTIL condition` - Post-condition loop

**Examples:**

```tc
LOOP i, 10          ; Loop while i < 10
    PRINT i
    INC i
ENDLOOP

WHILE counter > 0   ; Loop while counter > 0
    DEC counter
ENDWHILE

FOR i FROM 1 TO 10  ; i goes from 1 to 10
    PRINT i
ENDFOR

REPEAT              ; Execute at least once
    INC x
UNTIL x >= 5        ; Until x >= 5
```

---

## 7. Conditional Statements

- [x] `IF condition` / `ENDIF` - Execute if condition is true
- [x] `IF condition` / `ELSE` / `ENDIF` - Execute different blocks based on condition

**Examples:**

```tc
IF R1 > 10
    LOAD R2, 1
ENDIF

IF counter == 0
    PRINT R1
ELSE
    PRINT R2
ENDIF
```

---

## 8. Stack Operations

- [ ] `PUSH register` - Push register value onto stack
- [ ] `POP register` - Pop value from stack into register

**Examples:**

```tc
PUSH R1             ; Save R1 to stack
CALL my_function
POP R1              ; Restore R1 from stack
```

---

## 9. I/O Operations

- [x] `PRINT register` - Print register value to stdout
- [x] `PRINT identifier` - Print variable value to stdout
- [x] `PRINT immediate` - Print immediate value to stdout
- [x] `INPUT register` - Read integer from stdin to register
- [x] `INPUT identifier` - Read integer from stdin to variable

**Examples:**

```tc
PRINT R1            ; Print R1
PRINT counter       ; Print counter variable
PRINT 42            ; Print literal 42
INPUT R1            ; Read input into R1
INPUT user_value    ; Read input into user_value
```

---

## 10. Special Instructions

- [x] `HALT` - Terminate program execution
- [x] `NOP` - No operation (do nothing)

**Examples:**

```tc
HALT                ; Exit program
NOP                 ; Placeholder
```

---

## 11. Language Features

- [x] **Registers:** R1, R2, R3, R4, R5, R6, R7, R8
- [x] **Functions:** Named, reusable code blocks
- [x] **Comments:** `;` single-line comments
- [x] **Literals:** Decimal (42), Hex (0x2A), Binary (0b1010)
- [x] **Identifiers:** Letters, digits, underscore (must start with letter/underscore)

---

## Comparison Operators (for loops/conditionals)

- [x] `==` - Equal to
- [x] `!=` - Not equal to
- [x] `>` - Greater than
- [x] `<` - Less than
- [x] `>=` - Greater than or equal to
- [x] `<=` - Less than or equal to

---

## Complete Example Program

```tc
; Factorial calculator with function
FUNC factorial
    VAR result, 1
    VAR i, 1
    
    LOOP i, 6
        LOAD R1, result
        LOAD R2, i
        MUL R3, R1, R2
        SET result, R3
        INC i
    ENDLOOP
    
    LOAD R1, result
    RET R1
ENDFUNC

; Main program
CALL factorial
PRINT R1
HALT
```