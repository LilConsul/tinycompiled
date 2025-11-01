# TinyCompiled Instruction Set - Implementation Checklist

## 1. Variable Declaration
- [x] `VAR identifier` - Declare variable (default 0)
- [x] `VAR identifier, immediate` - Declare and initialize variable

## 2. Data Movement
- [x] `LOAD register, immediate` - Load immediate value into register
- [x] `LOAD register, identifier` - Load variable into register
- [x] `SET identifier, immediate` - Store immediate to variable
- [x] `SET identifier, register` - Store register to variable
- [x] `MOVE register, register` - Copy between registers

## 3. Arithmetic Operations
- [ ] `ADD register, register, register` - Addition (3 registers)
- [ ] `ADD register, register, immediate` - Addition (register + immediate)
- [ ] `SUB register, register, register` - Subtraction
- [ ] `SUB register, register, immediate` - Subtraction (register - immediate)
- [ ] `MUL register, register, register` - Multiplication
- [ ] `MUL register, register, immediate` - Multiplication (register * immediate)
- [ ] `DIV register, register, register` - Division
- [ ] `DIV register, register, immediate` - Division (register / immediate)
- [ ] `INC register` - Increment register
- [ ] `INC identifier` - Increment variable
- [ ] `DEC register` - Decrement register
- [ ] `DEC identifier` - Decrement variable

## 4. Logical/Bitwise Operations
- [ ] `AND register, register, register` - Bitwise AND
- [ ] `OR register, register, register` - Bitwise OR
- [ ] `XOR register, register, register` - Bitwise XOR
- [ ] `NOT register` - Bitwise NOT (in-place)
- [ ] `SHL register, register, immediate` - Shift left
- [ ] `SHR register, register, immediate` - Shift right

## 5. Comparison
- [ ] `CMP register, register` - Compare two registers
- [ ] `CMP register, immediate` - Compare register with immediate
- [ ] `CMP identifier, immediate` - Compare variable with immediate

## 6. Control Flow - Jumps
- [ ] `JMP label` - Unconditional jump
- [ ] `JE label` - Jump if equal
- [ ] `JNE label` - Jump if not equal
- [ ] `JG label` - Jump if greater
- [ ] `JL label` - Jump if less
- [ ] `JGE label` - Jump if greater or equal
- [ ] `JLE label` - Jump if less or equal

## 7. Functions
- [ ] `FUNC identifier` / `ENDFUNC` - Function definition
- [ ] `CALL identifier` - Call function
- [ ] `RET` - Return from function
- [ ] `RET register` - Return value in register

## 8. Loop Constructs
- [ ] `LOOP identifier, immediate` / `ENDLOOP` - Counted loop
- [ ] `WHILE condition` / `ENDWHILE` - Conditional loop
- [ ] `FOR identifier FROM immediate TO immediate` / `ENDFOR` - Range loop
- [ ] `FOR identifier FROM immediate TO immediate STEP immediate` / `ENDFOR` - Range loop with step
- [ ] `REPEAT` / `UNTIL condition` - Post-condition loop

## 9. Conditional Statements
- [ ] `IF condition` / `ENDIF` - Simple conditional
- [ ] `IF condition` / `ELSE` / `ENDIF` - Conditional with else

## 10. Stack Operations
- [ ] `PUSH register` - Push register to stack
- [ ] `POP register` - Pop from stack to register

## 11. I/O Operations
- [ ] `PRINT register` - Print register value
- [ ] `PRINT identifier` - Print variable value
- [ ] `PRINT immediate` - Print immediate value
- [ ] `INPUT register` - Read input to register
- [ ] `INPUT identifier` - Read input to variable

## 12. Special Instructions
- [ ] `HALT` - Terminate program
- [ ] `NOP` - No operation

## 13. Language Features
- [ ] **Registers:** R1, R2, R3, R4, R5, R6, R7, R8
- [ ] **Labels:** `label_name:` syntax (for jumps only)
- [ ] **Functions:** Named, reusable code blocks
- [ ] **Comments:** `;` single-line comments
- [ ] **Literals:** Decimal (42), Hex (0x2A), Binary (0b1010)
- [ ] **Identifiers:** Letters, digits, underscore (must start with letter/underscore)

---

## Comparison Operators (for loops/conditionals)
- [ ] `==` - Equal
- [ ] `!=` - Not equal
- [ ] `>` - Greater than
- [ ] `<` - Less than
- [ ] `>=` - Greater or equal
- [ ] `<=` - Less or equal

---
