from src.ast import *


class NasmGenerator:
    def __init__(self):
        self.data_section = []
        self.bss_section = []
        self.text_section = []
        self.label_counter = 0
        self.variables = {}
        self.needs_print_int = False
        self.needs_read_int = False
        self.register_map = {
            "R1": "rax",
            "R2": "rbx",
            "R3": "rcx",
            "R4": "rdx",
            "R5": "rsi",
            "R6": "rdi",
            "R7": "r8",
            "R8": "r9",
        }

    def get_register(self, reg: str) -> str:
        return self.register_map.get(reg, reg)

    def generate(self, ast: Program) -> str:
        # Add section headers first
        self.data_section.append("section .data")
        self.bss_section.append("section .bss")

        self.text_section.append("section .text")
        self.text_section.append("    global _start")
        self.text_section.append("")
        self.text_section.append("_start:")

        # Generate statements - this will populate sections
        for stmt in ast.statements:
            self.generate_statement(stmt)

        # Add I/O helper data after variables
        if self.needs_print_int:
            self.data_section.append("    newline db 10")
            self.data_section.append("    digit_buffer times 20 db 0")
        if self.needs_read_int:
            self.data_section.append("    input_buffer times 32 db 0")


        # Exit syscall
        self.text_section.append("    mov rax, 60")
        self.text_section.append("    mov rdi, 0")
        self.text_section.append("    syscall")

        # Add helper functions only if needed
        if self.needs_print_int or self.needs_read_int:
            self._add_helper_functions()

        output = []

        # Add data section if it has content beyond the header
        if len(self.data_section) > 1:
            output.extend(self.data_section)
            output.append("")

        # Add bss section if it has content beyond the header
        if len(self.bss_section) > 1:
            output.extend(self.bss_section)
            output.append("")

        output.extend(self.text_section)
        return "\n".join(output)

    def _add_helper_functions(self):
        """Add helper functions for syscall-based I/O"""

        if self.needs_print_int:
            # print_int: Convert integer in rax to string and print it
            self.text_section.append("")
            self.text_section.append("print_int:")
            self.text_section.append("    push rbp")
            self.text_section.append("    mov rbp, rsp")
            self.text_section.append("    push rbx")
            self.text_section.append("    push rcx")
            self.text_section.append("    push rdx")
            self.text_section.append("    push rsi")
            self.text_section.append("    push rdi")
            self.text_section.append("")
            self.text_section.append("    mov rbx, 10")
            self.text_section.append("    lea rsi, [digit_buffer + 19]")
            self.text_section.append("    mov byte [rsi], 0")
            self.text_section.append("    dec rsi")
            self.text_section.append("    mov rcx, 0")
            self.text_section.append("")
            self.text_section.append("    test rax, rax")
            self.text_section.append("    jns .positive")
            self.text_section.append("    neg rax")
            self.text_section.append("    mov rcx, 1")
            self.text_section.append("")
            self.text_section.append(".positive:")
            self.text_section.append("    xor rdx, rdx")
            self.text_section.append("    div rbx")
            self.text_section.append("    add dl, '0'")
            self.text_section.append("    mov [rsi], dl")
            self.text_section.append("    dec rsi")
            self.text_section.append("    test rax, rax")
            self.text_section.append("    jnz .positive")
            self.text_section.append("")
            self.text_section.append("    test rcx, rcx")
            self.text_section.append("    jz .print")
            self.text_section.append("    mov byte [rsi], '-'")
            self.text_section.append("    dec rsi")
            self.text_section.append("")
            self.text_section.append(".print:")
            self.text_section.append("    inc rsi")
            self.text_section.append("    mov rdx, digit_buffer + 19")
            self.text_section.append("    sub rdx, rsi")
            self.text_section.append("")
            self.text_section.append("    mov rax, 1")
            self.text_section.append("    mov rdi, 1")
            self.text_section.append("    syscall")
            self.text_section.append("")
            self.text_section.append("    mov rax, 1")
            self.text_section.append("    mov rdi, 1")
            self.text_section.append("    lea rsi, [newline]")
            self.text_section.append("    mov rdx, 1")
            self.text_section.append("    syscall")
            self.text_section.append("")
            self.text_section.append("    pop rdi")
            self.text_section.append("    pop rsi")
            self.text_section.append("    pop rdx")
            self.text_section.append("    pop rcx")
            self.text_section.append("    pop rbx")
            self.text_section.append("    pop rbp")
            self.text_section.append("    ret")

        if self.needs_read_int:
            # read_int: Read integer from stdin and return it in rax
            self.text_section.append("")
            self.text_section.append("read_int:")
            self.text_section.append("    push rbp")
            self.text_section.append("    mov rbp, rsp")
            self.text_section.append("    push rbx")
            self.text_section.append("    push rcx")
            self.text_section.append("    push rdx")
            self.text_section.append("    push rsi")
            self.text_section.append("    push rdi")
            self.text_section.append("")
            self.text_section.append("    mov rax, 0")
            self.text_section.append("    mov rdi, 0")
            self.text_section.append("    lea rsi, [input_buffer]")
            self.text_section.append("    mov rdx, 32")
            self.text_section.append("    syscall")
            self.text_section.append("")
            self.text_section.append("    lea rsi, [input_buffer]")
            self.text_section.append("    xor rax, rax")
            self.text_section.append("    xor rcx, rcx")
            self.text_section.append("    mov rbx, 10")
            self.text_section.append("")
            self.text_section.append("    movzx rdx, byte [rsi]")
            self.text_section.append("    cmp dl, '-'")
            self.text_section.append("    jne .parse_loop")
            self.text_section.append("    mov rcx, 1")
            self.text_section.append("    inc rsi")
            self.text_section.append("")
            self.text_section.append(".parse_loop:")
            self.text_section.append("    movzx rdx, byte [rsi]")
            self.text_section.append("    cmp dl, '0'")
            self.text_section.append("    jb .done")
            self.text_section.append("    cmp dl, '9'")
            self.text_section.append("    ja .done")
            self.text_section.append("    sub dl, '0'")
            self.text_section.append("    imul rax, rbx")
            self.text_section.append("    add rax, rdx")
            self.text_section.append("    inc rsi")
            self.text_section.append("    jmp .parse_loop")
            self.text_section.append("")
            self.text_section.append(".done:")
            self.text_section.append("    test rcx, rcx")
            self.text_section.append("    jz .return")
            self.text_section.append("    neg rax")
            self.text_section.append("")
            self.text_section.append(".return:")
            self.text_section.append("    pop rdi")
            self.text_section.append("    pop rsi")
            self.text_section.append("    pop rdx")
            self.text_section.append("    pop rcx")
            self.text_section.append("    pop rbx")
            self.text_section.append("    pop rbp")
            self.text_section.append("    ret")

    def generate_statement(self, stmt: ASTNode):
        if isinstance(stmt, VarDecl):
            self.generate_var_decl(stmt)
        elif isinstance(stmt, Load):
            self.generate_load(stmt)
        elif isinstance(stmt, Set):
            self.generate_set(stmt)
        elif isinstance(stmt, Print):
            self.generate_print(stmt)
        elif isinstance(stmt, Input):
            self.generate_input(stmt)
        elif isinstance(stmt, Halt):
            self.generate_halt()
        elif isinstance(stmt, Nop):
            self.text_section.append("    nop")

    def generate_var_decl(self, stmt: VarDecl):
        self.variables[stmt.name] = True
        if stmt.value is not None:
            self.data_section.append(f"    {stmt.name} dq {stmt.value}")
        else:
            self.bss_section.append(f"    {stmt.name} resq 1")

    def generate_load(self, stmt: Load):
        dest = self.get_register(stmt.dest)
        if isinstance(stmt.src, int):
            self.text_section.append(f"    mov {dest}, {stmt.src}")
        elif stmt.src in self.register_map:
            self.text_section.append(f"    mov {dest}, {self.get_register(stmt.src)}")
        else:
            self.text_section.append(f"    mov {dest}, [{stmt.src}]")

    def generate_set(self, stmt: Set):
        if isinstance(stmt.src, int):
            self.text_section.append(f"    mov qword [{stmt.dest}], {stmt.src}")
        else:
            self.text_section.append(
                f"    mov [{stmt.dest}], {self.get_register(stmt.src)}"
            )

    def generate_print(self, stmt: Print):
        self.needs_print_int = True

        # Save registers
        self.text_section.append("    push rax")
        self.text_section.append("    push rbx")
        self.text_section.append("    push rcx")
        self.text_section.append("    push rdx")
        self.text_section.append("    push rsi")
        self.text_section.append("    push rdi")

        # Load value to print into rax
        if isinstance(stmt.value, int):
            self.text_section.append(f"    mov rax, {stmt.value}")
        elif stmt.value in self.register_map:
            self.text_section.append(f"    mov rax, {self.get_register(stmt.value)}")
        else:
            self.text_section.append(f"    mov rax, [{stmt.value}]")

        # Convert integer to string and print
        self.text_section.append("    call print_int")

        # Restore registers
        self.text_section.append("    pop rdi")
        self.text_section.append("    pop rsi")
        self.text_section.append("    pop rdx")
        self.text_section.append("    pop rcx")
        self.text_section.append("    pop rbx")
        self.text_section.append("    pop rax")

    def generate_input(self, stmt: Input):
        self.needs_read_int = True

        # Save registers
        self.text_section.append("    push rax")
        self.text_section.append("    push rbx")
        self.text_section.append("    push rcx")
        self.text_section.append("    push rdx")
        self.text_section.append("    push rsi")
        self.text_section.append("    push rdi")

        # Read integer from stdin
        self.text_section.append("    call read_int")

        # Store result from rax to destination
        if stmt.dest in self.register_map:
            self.text_section.append(f"    mov r10, rax")
        else:
            self.text_section.append(f"    mov [r10], rax")

        # Restore registers
        self.text_section.append("    pop rdi")
        self.text_section.append("    pop rsi")
        self.text_section.append("    pop rdx")
        self.text_section.append("    pop rcx")
        self.text_section.append("    pop rbx")
        self.text_section.append("    pop rax")

        # Move result to final destination
        if stmt.dest in self.register_map:
            self.text_section.append(f"    mov {self.get_register(stmt.dest)}, r10")
        else:
            self.text_section.append(f"    mov [{stmt.dest}], r10")

    def generate_halt(self):
        self.text_section.append("    mov rax, 60")
        self.text_section.append("    mov rdi, 0")
        self.text_section.append("    syscall")
