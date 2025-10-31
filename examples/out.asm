section .data
    result dq 0
    newline db 10
    digit_buffer times 20 db 0

section .text
    global _start

_start:
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    mov rax, [result]
    call print_int
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    mov rax, 10
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    mov rax, rax
    call print_int
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    mov rbx, 20
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    mov rax, rbx
    call print_int
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    mov rax, [result]
    call print_int
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    mov rax, 60
    mov rdi, 0
    syscall
    mov rax, 60
    mov rdi, 0
    syscall

print_int:
    push rbp
    mov rbp, rsp
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi

    mov rbx, 10
    lea rsi, [digit_buffer + 19]
    mov byte [rsi], 0
    dec rsi
    mov rcx, 0

    test rax, rax
    jns .positive
    neg rax
    mov rcx, 1

.positive:
    xor rdx, rdx
    div rbx
    add dl, '0'
    mov [rsi], dl
    dec rsi
    test rax, rax
    jnz .positive

    test rcx, rcx
    jz .print
    mov byte [rsi], '-'
    dec rsi

.print:
    inc rsi
    mov rdx, digit_buffer + 19
    sub rdx, rsi

    mov rax, 1
    mov rdi, 1
    syscall

    mov rax, 1
    mov rdi, 1
    lea rsi, [newline]
    mov rdx, 1
    syscall

    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rbp
    ret