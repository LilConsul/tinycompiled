from src.ast import *


class NasmGenerator:
    """NASM x86-64 assembly code generator"""

    # Syscall numbers for Linux x86-64
    SYS_READ = 0
    SYS_WRITE = 1
    SYS_EXIT = 60

    # File descriptors
    STDIN = 0
    STDOUT = 1

    # Buffer sizes
    DIGIT_BUFFER_SIZE = 20
    INPUT_BUFFER_SIZE = 32

    # Register mapping for virtual registers
    REGISTER_MAP = {
        "R1": "rax",
        "R2": "rbx",
        "R3": "rcx",
        "R4": "rdx",
        "R5": "rsi",
        "R6": "rdi",
        "R7": "r8",
        "R8": "r9",
    }

    def __init__(self):
        self.data_section = []
        self.bss_section = []
        self.text_section = []
        self.label_counter = 0
        self.variables = {}
        self.needs_print_int = False
        self.needs_read_int = False

    def get_register(self, reg: str) -> str:
        """Convert virtual register name to actual x86-64 register"""
        return self.REGISTER_MAP.get(reg, reg)

    def is_register(self, operand: str) -> bool:
        """Check if operand is a register"""
        return operand in self.REGISTER_MAP

    def emit_data(self, line: str):
        """Add a line to the data section"""
        self.data_section.append(f"    {line}")

    def emit_bss(self, line: str):
        """Add a line to the bss section"""
        self.bss_section.append(f"    {line}")

    def emit(self, instruction: str, indent: bool = True):
        """Add an instruction to the text section"""
        prefix = "    " if indent else ""
        self.text_section.append(f"{prefix}{instruction}")

    def emit_label(self, label: str):
        """Add a label to the text section"""
        self.text_section.append(f"{label}:")

    def generate(self, ast: Program) -> str:
        """Generate NASM assembly code from AST"""
        self._initialize_sections()
        self._generate_program_body(ast)
        self._finalize_program()
        return self._build_output()

    def _initialize_sections(self):
        """Set up section headers"""
        self.data_section.append("section .data")
        self.bss_section.append("section .bss")
        self.text_section.append("section .text")
        self.emit("global _start", )
        self.text_section.append("")
        self.emit_label("_start")

    def _generate_program_body(self, ast: Program):
        """Generate code for all statements in the program"""
        for stmt in ast.statements:
            self.generate_statement(stmt)

    def _finalize_program(self):
        """Add I/O buffers, exit code, and helper functions"""
        self._add_io_buffers()
        self._add_exit_code()
        self._add_helper_functions()

    def _add_io_buffers(self):
        """Add data buffers needed for I/O operations"""
        if self.needs_print_int:
            self.emit_data("newline db 10")
            self.emit_data(f"digit_buffer times {self.DIGIT_BUFFER_SIZE} db 0")
        if self.needs_read_int:
            self.emit_data(f"input_buffer times {self.INPUT_BUFFER_SIZE} db 0")

    def _add_exit_code(self):
        """Add program exit syscall"""
        self.emit(f"mov rax, {self.SYS_EXIT}")
        self.emit("mov rdi, 0")
        self.emit("syscall")

    def _build_output(self) -> str:
        """Assemble final output from all sections"""
        output = []

        if len(self.data_section) > 1:
            output.extend(self.data_section)
            output.append("")

        if len(self.bss_section) > 1:
            output.extend(self.bss_section)
            output.append("")

        output.extend(self.text_section)
        return "\n".join(output)

    def _add_helper_functions(self):
        """Add helper functions for syscall-based I/O"""
        if self.needs_print_int:
            self._add_print_int_function()
        if self.needs_read_int:
            self._add_read_int_function()

    def _add_print_int_function(self):
        """Generate print_int helper: converts integer in rax to string and prints it"""
        self.text_section.append("")
        self.emit_label("print_int")

        # Function prologue
        self._emit_function_prologue()

        # Convert integer to string (reverse order in buffer)
        self.emit("mov rbx, 10")
        self.emit(f"lea rsi, [digit_buffer + {self.DIGIT_BUFFER_SIZE - 1}]")
        self.emit("mov byte [rsi], 0")
        self.emit("dec rsi")
        self.emit("mov rcx, 0  ; sign flag")
        self.text_section.append("")

        # Handle negative numbers
        self.emit("test rax, rax")
        self.emit("jns .positive")
        self.emit("neg rax")
        self.emit("mov rcx, 1")
        self.text_section.append("")

        # Convert digits
        self.emit_label(".positive")
        self.emit("xor rdx, rdx")
        self.emit("div rbx")
        self.emit("add dl, '0'")
        self.emit("mov [rsi], dl")
        self.emit("dec rsi")
        self.emit("test rax, rax")
        self.emit("jnz .positive")
        self.text_section.append("")

        # Add minus sign if needed
        self.emit("test rcx, rcx")
        self.emit("jz .print")
        self.emit("mov byte [rsi], '-'")
        self.emit("dec rsi")
        self.text_section.append("")

        # Print the string
        self.emit_label(".print")
        self.emit("inc rsi")
        self.emit(f"mov rdx, digit_buffer + {self.DIGIT_BUFFER_SIZE - 1}")
        self.emit("sub rdx, rsi")
        self._emit_write_syscall()

        # Print newline
        self.emit(f"mov rax, {self.SYS_WRITE}")
        self.emit(f"mov rdi, {self.STDOUT}")
        self.emit("lea rsi, [newline]")
        self.emit("mov rdx, 1")
        self.emit("syscall")
        self.text_section.append("")

        # Function epilogue
        self._emit_function_epilogue()

    def _add_read_int_function(self):
        """Generate read_int helper: reads integer from stdin and returns it in rax"""
        self.text_section.append("")
        self.emit_label("read_int")

        # Function prologue
        self._emit_function_prologue()

        # Read from stdin
        self.emit(f"mov rax, {self.SYS_READ}")
        self.emit(f"mov rdi, {self.STDIN}")
        self.emit("lea rsi, [input_buffer]")
        self.emit(f"mov rdx, {self.INPUT_BUFFER_SIZE}")
        self.emit("syscall")
        self.text_section.append("")

        # Parse string to integer
        self.emit("lea rsi, [input_buffer]")
        self.emit("xor rax, rax")
        self.emit("xor rcx, rcx  ; sign flag")
        self.emit("mov rbx, 10")
        self.text_section.append("")

        # Check for negative sign
        self.emit("movzx rdx, byte [rsi]")
        self.emit("cmp dl, '-'")
        self.emit("jne .parse_loop")
        self.emit("mov rcx, 1")
        self.emit("inc rsi")
        self.text_section.append("")

        # Parse digits
        self.emit_label(".parse_loop")
        self.emit("movzx rdx, byte [rsi]")
        self.emit("cmp dl, '0'")
        self.emit("jb .done")
        self.emit("cmp dl, '9'")
        self.emit("ja .done")
        self.emit("sub dl, '0'")
        self.emit("imul rax, rbx")
        self.emit("add rax, rdx")
        self.emit("inc rsi")
        self.emit("jmp .parse_loop")
        self.text_section.append("")

        # Apply sign
        self.emit_label(".done")
        self.emit("test rcx, rcx")
        self.emit("jz .return")
        self.emit("neg rax")
        self.text_section.append("")

        # Function epilogue
        self.emit_label(".return")
        self._emit_function_epilogue()

    def _emit_function_prologue(self):
        """Emit standard function prologue with register preservation"""
        self.emit("push rbp")
        self.emit("mov rbp, rsp")
        self.emit("push rbx")
        self.emit("push rcx")
        self.emit("push rdx")
        self.emit("push rsi")
        self.emit("push rdi")
        self.text_section.append("")

    def _emit_function_epilogue(self):
        """Emit standard function epilogue with register restoration"""
        self.emit("pop rdi")
        self.emit("pop rsi")
        self.emit("pop rdx")
        self.emit("pop rcx")
        self.emit("pop rbx")
        self.emit("pop rbp")
        self.emit("ret")

    def _emit_write_syscall(self):
        """Emit write syscall to stdout"""
        self.emit(f"mov rax, {self.SYS_WRITE}")
        self.emit(f"mov rdi, {self.STDOUT}")
        self.emit("syscall")
        self.text_section.append("")

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
        """Generate variable declaration in data or bss section"""
        self.variables[stmt.name] = True
        if stmt.value is not None:
            self.emit_data(f"{stmt.name} dq {stmt.value}")
        else:
            self.emit_bss(f"{stmt.name} resq 1")

    def generate_load(self, stmt: Load):
        """Generate LOAD instruction: load value into register"""
        dest = self.get_register(stmt.dest)

        if isinstance(stmt.src, int):
            self.emit(f"mov {dest}, {stmt.src}")
        elif self.is_register(stmt.src):
            self.emit(f"mov {dest}, {self.get_register(stmt.src)}")
        else:
            self.emit(f"mov {dest}, [{stmt.src}]")

    def generate_set(self, stmt: Set):
        """Generate SET instruction: store value to memory"""
        if isinstance(stmt.src, int):
            self.emit(f"mov qword [{stmt.dest}], {stmt.src}")
        else:
            self.emit(f"mov [{stmt.dest}], {self.get_register(stmt.src)}")

    def generate_print(self, stmt: Print):
        """Generate PRINT instruction: output integer value"""
        self.needs_print_int = True

        self._load_value_to_rax(stmt.value)
        self.emit("call print_int")

    def generate_input(self, stmt: Input):
        """Generate INPUT instruction: read integer from stdin"""
        self.needs_read_int = True

        self.emit("call read_int")

        # Store result from rax to destination
        if self.is_register(stmt.dest):
            self.emit(f"mov {self.get_register(stmt.dest)}, rax")
        else:
            self.emit(f"mov [{stmt.dest}], rax")

    def generate_halt(self):
        """Generate HALT instruction: exit program"""
        self.emit(f"mov rax, {self.SYS_EXIT}")
        self.emit("mov rdi, 0")
        self.emit("syscall")

    def _load_value_to_rax(self, value):
        """Load a value (immediate, register, or variable) into rax"""
        if isinstance(value, int):
            self.emit(f"mov rax, {value}")
        elif self.is_register(value):
            self.emit(f"mov rax, {self.get_register(value)}")
        else:
            self.emit(f"mov rax, [{value}]")

    def _save_all_registers(self):
        """Save all general-purpose registers on the stack"""
        for reg in self.REGISTER_MAP.values():
            self.emit(f"push {reg}")

    def _restore_all_registers(self):
        """Restore all general-purpose registers from the stack"""
        for reg in reversed(list(self.REGISTER_MAP.values())):
            self.emit(f"pop {reg}")
