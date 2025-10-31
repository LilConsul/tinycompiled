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
        """Generate print_int helper: converts integer in r15 to string and prints it
        Takes argument in r15, uses only scratch registers r10-r15 to preserve user's R1-R8 registers
        Note: syscall destroys rcx and r11, so we save/restore them"""
        self.text_section.append("")
        self.emit_label("print_int")

        # Save registers that syscall will destroy (rcx=R3, r11)
        self.emit("push rcx")
        self.emit("push r11")
        self.text_section.append("")

        # r15 contains the value to print (passed by caller)
        # r10 = working value, r11 = divisor (10), r12 = buffer pointer, r13 = sign flag
        self.emit("mov r10, r15")
        self.text_section.append("")

        # Convert integer to string (reverse order in buffer)
        self.emit("mov r11, 10")
        self.emit(f"lea r12, [digit_buffer + {self.DIGIT_BUFFER_SIZE - 1}]")
        self.emit("mov byte [r12], 0")
        self.emit("dec r12")
        self.emit("xor r13, r13  ; sign flag")
        self.text_section.append("")

        # Handle negative numbers
        self.emit("test r10, r10")
        self.emit("jns .positive")
        self.emit("neg r10")
        self.emit("mov r13, 1")
        self.text_section.append("")

        # Convert digits - need to use rax/rdx for division
        self.emit_label(".positive")
        self.emit("mov rax, r10")
        self.emit("xor rdx, rdx")
        self.emit("div r11")
        self.emit("mov r10, rax  ; quotient back to r10")
        self.emit("add dl, '0'")
        self.emit("mov [r12], dl")
        self.emit("dec r12")
        self.emit("test r10, r10")
        self.emit("jnz .positive")
        self.text_section.append("")

        # Add minus sign if needed
        self.emit("test r13, r13")
        self.emit("jz .print")
        self.emit("mov byte [r12], '-'")
        self.emit("dec r12")
        self.text_section.append("")

        # Print the string - syscall clobbers rax, rdi, rsi, rdx but we don't care
        self.emit_label(".print")
        self.emit("inc r12  ; r12 = start of string")
        self.emit(f"mov rdx, digit_buffer + {self.DIGIT_BUFFER_SIZE - 1}")
        self.emit("sub rdx, r12  ; rdx = length")
        self.emit("mov rsi, r12  ; rsi = buffer pointer")
        self.emit(f"mov rax, {self.SYS_WRITE}")
        self.emit(f"mov rdi, {self.STDOUT}")
        self.emit("syscall")
        self.text_section.append("")

        # Print newline
        self.emit(f"mov rax, {self.SYS_WRITE}")
        self.emit(f"mov rdi, {self.STDOUT}")
        self.emit("lea rsi, [newline]")
        self.emit("mov rdx, 1")
        self.emit("syscall")
        self.text_section.append("")

        # Restore registers
        self.emit("pop r11")
        self.emit("pop rcx")
        self.text_section.append("")

        self.emit("ret")

    def _add_read_int_function(self):
        """Generate read_int helper: reads integer from stdin and returns it in r15
        Uses only scratch registers r10-r15 to preserve user's R1-R8 registers"""
        self.text_section.append("")
        self.emit_label("read_int")

        # Read from stdin using syscall (clobbers rax, rdi, rsi, rdx but we don't care)
        self.emit(f"mov rax, {self.SYS_READ}")
        self.emit(f"mov rdi, {self.STDIN}")
        self.emit("lea rsi, [input_buffer]")
        self.emit(f"mov rdx, {self.INPUT_BUFFER_SIZE}")
        self.emit("syscall")
        self.text_section.append("")

        # Parse string to integer using scratch registers
        # r10 = result accumulator, r11 = multiplier (10), r12 = buffer pointer
        # r13 = sign flag, r14 = temp for current digit
        self.emit("lea r12, [input_buffer]")
        self.emit("xor r10, r10  ; result = 0")
        self.emit("xor r13, r13  ; sign flag = 0")
        self.emit("mov r11, 10")
        self.text_section.append("")

        # Check for negative sign
        self.emit("movzx r14, byte [r12]")
        self.emit("cmp r14b, '-'")
        self.emit("jne .parse_loop")
        self.emit("mov r13, 1  ; set sign flag")
        self.emit("inc r12")
        self.text_section.append("")

        # Parse digits
        self.emit_label(".parse_loop")
        self.emit("movzx r14, byte [r12]")
        self.emit("cmp r14b, '0'")
        self.emit("jb .done")
        self.emit("cmp r14b, '9'")
        self.emit("ja .done")
        self.emit("sub r14b, '0'")
        self.emit("imul r10, r11  ; result *= 10")
        self.emit("add r10, r14   ; result += digit")
        self.emit("inc r12")
        self.emit("jmp .parse_loop")
        self.text_section.append("")

        # Apply sign and return result in r15
        self.emit_label(".done")
        self.emit("mov r15, r10")
        self.emit("test r13, r13")
        self.emit("jz .return")
        self.emit("neg r15")
        self.text_section.append("")

        self.emit_label(".return")
        self.emit("ret")



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
        elif isinstance(stmt, BinaryOp):
            self.generate_binary_op(stmt)
        elif isinstance(stmt, Halt):
            self.generate_halt()
        elif isinstance(stmt, Nop):
            self.text_section.append("    nop")

    def generate_binary_op(self, stmt: BinaryOp):
        """Generate binary operation instruction"""
        dest = self.get_register(stmt.dest)
        left = self.get_register(stmt.left)

        # Load left operand into destination register
        if dest != left:
            self.emit(f"mov {dest}, {left}")

        # Determine right operand
        if isinstance(stmt.right, int):
            right_operand = str(stmt.right)
        elif self.is_register(stmt.right):
            right_operand = self.get_register(stmt.right)
        else:
            right_operand = f"[{stmt.right}]"

        # Generate operation
        if stmt.op == "ADD":
            self.emit(f"add {dest}, {right_operand}")
        elif stmt.op == "SUB":
            self.emit(f"sub {dest}, {right_operand}")
        elif stmt.op == "MUL":
            self.emit(f"imul {dest}, {right_operand}")
        elif stmt.op == "DIV":
            self.emit("xor rdx, rdx")  # Clear rdx before division
            if right_operand.isdigit():
                self.emit(f"mov rbx, {right_operand}")
                self.emit(f"div rbx")
            else:
                self.emit(f"div {right_operand}")
        elif stmt.op == "AND":
            self.emit(f"and {dest}, {right_operand}")
        elif stmt.op == "OR":
            self.emit(f"or {dest}, {right_operand}")
        elif stmt.op == "XOR":
            self.emit(f"xor {dest}, {right_operand}")

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
            self.emit(f"mov qword [{stmt.dest}], {self.get_register(stmt.src)}")

    def generate_print(self, stmt: Print):
        """Generate PRINT instruction: output integer value"""
        self.needs_print_int = True

        # Load value to r15 (scratch register) to avoid clobbering R1-R8
        self._load_value_to_r15(stmt.value)
        self.emit("call print_int")

    def generate_input(self, stmt: Input):
        """Generate INPUT instruction: read integer from stdin"""
        self.needs_read_int = True

        self.emit("call read_int")

        # Store result from r15 (scratch register) to destination
        if self.is_register(stmt.dest):
            self.emit(f"mov {self.get_register(stmt.dest)}, r15")
        else:
            self.emit(f"mov [{stmt.dest}], r15")

    def generate_halt(self):
        """Generate HALT instruction: exit program"""
        self.emit(f"mov rax, {self.SYS_EXIT}")
        self.emit("mov rdi, 0")
        self.emit("syscall")

    def _load_value_to_r15(self, value):
        """Load a value (immediate, register, or variable) into r15 (scratch register)"""
        if isinstance(value, int):
            self.emit(f"mov r15, {value}")
        elif self.is_register(value):
            self.emit(f"mov r15, {self.get_register(value)}")
        else:
            self.emit(f"mov r15, [{value}]")

