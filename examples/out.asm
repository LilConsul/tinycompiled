section .data
    result dq 0
    newline db 10
    digit_buffer times 20 db 0

section .text
    global _start

_start:
    mov rax, [result]
    call print_int
    mov rax, 10
    mov rax, rax
    call print_int
    mov rbx, 20
    mov rax, rbx
    call print_int
    mov rax, [result]
    call print_int
    mov rax, 60
    mov rdi, 0
    syscall
    mov rax, 60
    mov rdi, 0
    syscall

print_int:
    mov r10, rax

    mov r11, 10
    lea r12, [digit_buffer + 19]
    mov byte [r12], 0
    dec r12
    xor r13, r13  ; sign flag

    test r10, r10
    jns .positive
    neg r10
    mov r13, 1

.positive:
    mov rax, r10
    xor rdx, rdx
    div r11
    mov r10, rax  ; quotient back to r10
    add dl, '0'
    mov [r12], dl
    dec r12
    test r10, r10
    jnz .positive

    test r13, r13
    jz .print
    mov byte [r12], '-'
    dec r12

.print:
    inc r12  ; r12 = start of string
    mov rdx, digit_buffer + 19
    sub rdx, r12  ; rdx = length
    mov rsi, r12  ; rsi = buffer pointer
    mov rax, 1
    mov rdi, 1
    syscall

    mov rax, 1
    mov rdi, 1
    lea rsi, [newline]
    mov rdx, 1
    syscall

    ret