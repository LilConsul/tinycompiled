section .data
    hello: db 'Hello world', 0x0A ; Define a string with a newline character
    helloLen: equ $-hello         ; Calculate string length

section .text
    global _start                 ; Entry point for the program

_start:
    mov eax, 4                    ; System call number (sys_write)
    mov ebx, 1                    ; File descriptor (stdout)
    mov ecx, hello                ; Pointer to the string
    mov edx, helloLen             ; Length of the string
    int 0x80                      ; Call kernel

    mov eax, 1                    ; System call number (sys_exit)
    xor ebx, ebx                  ; Exit code 0
    int 0x80                      ; Call kernel

