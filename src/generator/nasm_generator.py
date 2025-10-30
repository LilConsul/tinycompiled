from src.ast import *


class NasmGenerator:
    def __init__(self):
        self.data_section = []
        self.bss_section = []
        self.text_section = []
        self.label_counter = 0
        self.variables = {}
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
        self.data_section.append("section .data")
        self.data_section.append("    newline db 10")
        self.data_section.append('    fmt_int db "%ld", 10, 0')
        self.data_section.append('    fmt_read db "%ld", 0')

        self.text_section.append("section .text")
        self.text_section.append("    global _start")
        self.text_section.append("    extern printf, scanf, exit")
        self.text_section.append("")
        self.text_section.append("_start:")

        for stmt in ast.statements:
            self.generate_statement(stmt)

        self.text_section.append("    mov rdi, 0")
        self.text_section.append("    call exit")

        output = []
        output.extend(self.data_section)
        output.append("")
        if self.bss_section:
            output.append("section .bss")
            output.extend(self.bss_section)
            output.append("")
        output.extend(self.text_section)
        return "\n".join(output)

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
        self.text_section.append("    push rdi")
        self.text_section.append("    push rsi")
        self.text_section.append("    push rax")
        if isinstance(stmt.value, int):
            self.text_section.append(f"    mov rsi, {stmt.value}")
        elif stmt.value in self.register_map:
            self.text_section.append(f"    mov rsi, {self.get_register(stmt.value)}")
        else:
            self.text_section.append(f"    mov rsi, [{stmt.value}]")
        self.text_section.append("    mov rdi, fmt_int")
        self.text_section.append("    xor rax, rax")
        self.text_section.append("    call printf")
        self.text_section.append("    pop rax")
        self.text_section.append("    pop rsi")
        self.text_section.append("    pop rdi")

    def generate_input(self, stmt: Input):
        self.text_section.append("    push rdi")
        self.text_section.append("    push rsi")
        self.text_section.append("    push rax")
        self.text_section.append("    sub rsp, 8")
        self.text_section.append("    mov rdi, fmt_read")
        self.text_section.append("    mov rsi, rsp")
        self.text_section.append("    xor rax, rax")
        self.text_section.append("    call scanf")
        self.text_section.append("    mov r10, [rsp]")
        self.text_section.append("    add rsp, 8")
        if stmt.dest in self.register_map:
            self.text_section.append(f"    mov {self.get_register(stmt.dest)}, r10")
        else:
            self.text_section.append(f"    mov [{stmt.dest}], r10")
        self.text_section.append("    pop rax")
        self.text_section.append("    pop rsi")
        self.text_section.append("    pop rdi")

    def generate_halt(self):
        self.text_section.append("    mov rdi, 0")
        self.text_section.append("    call exit")
