section .data
    newline db 10
    fmt_int db "%ld", 10, 0
    fmt_read db "%ld", 0
    result dq 0

section .text
    global _start
    extern printf, scanf, exit

_start:
    push rdi
    push rsi
    push rax
    mov rsi, [result]
    mov rdi, fmt_int
    xor rax, rax
    call printf
    pop rax
    pop rsi
    pop rdi
    mov rax, 10
    push rdi
    push rsi
    push rax
    mov rsi, rax
    mov rdi, fmt_int
    xor rax, rax
    call printf
    pop rax
    pop rsi
    pop rdi
    mov rbx, 20
    push rdi
    push rsi
    push rax
    mov rsi, rax
    mov rdi, fmt_int
    xor rax, rax
    call printf
    pop rax
    pop rsi
    pop rdi
    push rdi
    push rsi
    push rax
    mov rsi, [result]
    mov rdi, fmt_int
    xor rax, rax
    call printf
    pop rax
    pop rsi
    pop rdi
    mov rdi, 0
    call exit
    mov rdi, 0
    call exit