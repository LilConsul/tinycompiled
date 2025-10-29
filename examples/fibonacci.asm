section .data
    a dq 0
    b dq 1
    temp dq 0
    count dq 0
    newline db 0x0A

section .bss
    num_buffer resb 20

section .text
    global _start

_start:
    ; PRINT a
    mov rax, [a]
    call print_num
    
    ; PRINT b
    mov rax, [b]
    call print_num
    
.loop_start:
    ; LOOP count, 8
    mov rax, [count]
    cmp rax, 8
    jge .loop_end
    
    ; LOAD R1, a
    mov rax, [a]
    ; LOAD R2, b
    mov rbx, [b]
    ; ADD R3, R1, R2
    mov rcx, rax
    add rcx, rbx
    ; SET temp, R3
    mov [temp], rcx
    
    ; SET a, b
    mov rax, [b]
    mov [a], rax
    ; SET b, temp
    mov rax, [temp]
    mov [b], rax
    
    ; PRINT temp
    mov rax, [temp]
    call print_num
    
    ; INC count
    mov rax, [count]
    inc rax
    mov [count], rax
    
    jmp .loop_start

.loop_end:
    ; HALT
    mov eax, 1
    xor ebx, ebx
    int 0x80

print_num:
    push rbp
    push rax
    push rbx
    push rcx
    push rdx
    
    mov rbp, num_buffer
    add rbp, 19
    mov byte [rbp], 0
    mov rbx, 10
    
.div_loop:
    xor rdx, rdx
    div rbx
    add dl, '0'
    dec rbp
    mov [rbp], dl
    test rax, rax
    jnz .div_loop
    
    ; Calculate length
    mov rax, num_buffer
    add rax, 19
    sub rax, rbp
    mov rdx, rax
    
    ; sys_write
    mov eax, 4
    mov ebx, 1
    mov ecx, ebp
    int 0x80
    
    ; Print newline
    mov eax, 4
    mov ebx, 1
    mov ecx, newline
    mov edx, 1
    int 0x80
    
    pop rdx
    pop rcx
    pop rbx
    pop rax
    pop rbp
    ret
