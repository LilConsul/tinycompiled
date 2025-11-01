; TinyCompiled Language - Tree-sitter Syntax Highlighting Queries

; Comments
(comment) @comment

; Keywords - Control Flow
[
  "IF"
  "ELSE"
  "ENDIF"
  "WHILE"
  "ENDWHILE"
  "FOR"
  "ENDFOR"
  "LOOP"
  "ENDLOOP"
  "REPEAT"
  "UNTIL"
] @keyword.control.conditional

; Keywords - Function
[
  "FUNC"
  "ENDFUNC"
  "CALL"
  "RET"
] @keyword.function

; Keywords - Jump/Branch
[
  "JMP"
  "JE"
  "JNE"
  "JG"
  "JL"
  "JGE"
  "JLE"
] @keyword.control.jump

; Keywords - Variable and Memory
[
  "VAR"
  "LOAD"
  "SET"
  "MOVE"
  "PUSH"
  "POP"
] @keyword.storage

; Keywords - Arithmetic Operations
[
  "ADD"
  "SUB"
  "MUL"
  "DIV"
  "INC"
  "DEC"
] @keyword.operator.arithmetic

; Keywords - Logical Operations
[
  "AND"
  "OR"
  "XOR"
  "NOT"
  "CMP"
] @keyword.operator.logical

; Keywords - Bitwise Operations
[
  "SHL"
  "SHR"
] @keyword.operator.bitwise

; Keywords - I/O and System
[
  "PRINT"
  "INPUT"
  "HALT"
  "NOP"
] @keyword.other

; Registers (R1-R8)
(register) @variable.builtin

; Labels (name followed by colon)
(label_definition
  name: (identifier) @label)

; Label references
(label_reference) @label

; Identifiers (variable names)
(identifier) @variable

; Numbers
(number) @constant.numeric

; Hexadecimal numbers
(hex_number) @constant.numeric.hex

; Binary numbers
(binary_number) @constant.numeric.binary

; Operators
[
  "=="
  "!="
  ">"
  "<"
  ">="
  "<="
] @operator.comparison

; Punctuation
[
  ","
  ":"
] @punctuation.delimiter

; Special highlighting for specific constructs
(var_declaration
  name: (identifier) @variable.declaration)

(set_statement
  target: (identifier) @variable)

(load_statement
  register: (register) @variable.builtin)

(binary_operation
  operator: [
    "ADD"
    "SUB"
    "MUL"
    "DIV"
    "AND"
    "OR"
    "XOR"
  ] @keyword.operator)

; Function calls
(call_statement
  function: (identifier) @function.call)

; Print and input statements
(print_statement
  value: (_) @variable.parameter)

(input_statement
  target: (_) @variable.parameter)

