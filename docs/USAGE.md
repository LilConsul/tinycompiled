## Function Example

```tc
; Function to calculate factorial
FUNC factorial
    LOAD R1, n
    LOAD R2, 1
    
    LOOP R1, 1
        MUL R2, R2, R1
        DEC R1
    ENDLOOP
    
    RET R2
ENDFUNC

; Main program
VAR n, 5
CALL factorial
PRINT R2
HALT
```