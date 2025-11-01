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
        self.functions = []

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
        self.emit(
            "global _start",
        )
        self.text_section.append("")
        self.emit_label("_start")
        self.emit("jmp main_code")

    def _generate_program_body(self, ast: Program):
        """Generate code for all statements in the program"""
        self.emit_label("main_code")
        for stmt in ast.statements:
            self.generate_statement(stmt)
        for func in self.functions:
            self.generate_function(func)

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
        Note: We use rax, rbx, rdx, rsi, rdi, rcx, r11 internally, so we must save them"""
        self.text_section.append("")
        self.emit_label("print_int")

        # Save all registers we will use (R1-R6 mapping)
        self.emit("push rax")  # R1
        self.emit("push rbx")  # R2
        self.emit("push rcx")  # R3
        self.emit("push rdx")  # R4
        self.emit("push rsi")  # R5
        self.emit("push rdi")  # R6
        self.emit("push r11")  # scratch for divisor
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

        # Restore registers in reverse order (LIFO)
        self.emit("pop r11")
        self.emit("pop rdi")  # R6
        self.emit("pop rsi")  # R5
        self.emit("pop rdx")  # R4
        self.emit("pop rcx")  # R3
        self.emit("pop rbx")  # R2
        self.emit("pop rax")  # R1
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
        if isinstance(stmt, Function):
            self.functions.append(stmt)
            return
        elif isinstance(stmt, VarDecl):
            self.generate_var_decl(stmt)
        elif isinstance(stmt, Load):
            self.generate_load(stmt)
        elif isinstance(stmt, Set):
            self.generate_set(stmt)
        elif isinstance(stmt, Move):
            self.generate_move(stmt)
        elif isinstance(stmt, Print):
            self.generate_print(stmt)
        elif isinstance(stmt, Input):
            self.generate_input(stmt)
        elif isinstance(stmt, BinaryOp):
            self.generate_binary_op(stmt)
        elif isinstance(stmt, UnaryOp):
            self.generate_unary_op(stmt)
        elif isinstance(stmt, ShiftOp):
            self.generate_shift(stmt)
        elif isinstance(stmt, Halt):
            self.generate_halt()
        elif isinstance(stmt, Nop):
            self.text_section.append("    nop")
        elif isinstance(stmt, Call):
            self.generate_call(stmt)
        elif isinstance(stmt, Return):
            self.generate_return(stmt)
        elif isinstance(stmt, If):
            self.generate_if(stmt)
        elif isinstance(stmt, Loop):
            self.generate_loop(stmt)
        elif isinstance(stmt, While):
            self.generate_while(stmt)
        elif isinstance(stmt, For):
            self.generate_for(stmt)
        elif isinstance(stmt, Repeat):
            self.generate_repeat(stmt)

    def generate_unary_op(self, stmt: UnaryOp):
        """Generate unary operation instruction"""
        operand = self.get_register(stmt.operand)

        if stmt.op == "INC":
            self.emit(f"inc {operand}")
        elif stmt.op == "DEC":
            self.emit(f"dec {operand}")
        elif stmt.op == "NOT":
            self.emit(f"not {operand}")

    def generate_shift(self, stmt: ShiftOp):
        """Generate shift operation instruction"""
        dest = self.get_register(stmt.dest)
        src = self.get_register(stmt.src)
        count = stmt.count

        # Move src to dest if not the same
        if dest != src:
            self.emit(f"mov {dest}, {src}")

        # Perform shift
        if stmt.op == "SHL":
            self.emit(f"shl {dest}, {count}")
        elif stmt.op == "SHR":
            self.emit(f"shr {dest}, {count}")

    def generate_binary_op(self, stmt: BinaryOp):
        """Generate binary operation instruction"""
        dest = self.get_register(stmt.dest)
        left = self.get_register(stmt.left)

        # Determine right operand
        if isinstance(stmt.right, int):
            right_operand = str(stmt.right)
        elif self.is_register(stmt.right):
            right_operand = self.get_register(stmt.right)
        else:
            right_operand = f"[{stmt.right}]"

        # DIV is special - it uses rax/rdx implicitly
        if stmt.op == "DIV":
            # Always save rdx since DIV clobbers it
            if dest != "rdx":
                self.emit("push rdx")

            # Save rax if we'll clobber it and it's not the destination
            # This includes the case where left == rax but dest != rax
            save_rax = dest != "rax"
            if save_rax:
                self.emit("push rax")

            # Move dividend to rax if not already there
            if left != "rax":
                self.emit(f"mov rax, {left}")

            # Clear rdx for unsigned division
            self.emit("xor rdx, rdx")

            # Perform division
            if isinstance(stmt.right, int):
                # Immediate values need to go through a register
                self.emit("push r10")
                self.emit(f"mov r10, {stmt.right}")
                self.emit("div r10")
                self.emit("pop r10")
            else:
                self.emit(f"div {right_operand}")

            # Move quotient to destination if not rax
            if dest != "rax":
                self.emit(f"mov {dest}, rax")

            # Restore rax if we saved it
            if save_rax:
                self.emit("pop rax")

            # Restore rdx
            if dest != "rdx":
                self.emit("pop rdx")
        else:
            # For other operations, load left operand into destination register
            if dest != left:
                self.emit(f"mov {dest}, {left}")

            # Generate operation
            if stmt.op == "ADD":
                self.emit(f"add {dest}, {right_operand}")
            elif stmt.op == "SUB":
                self.emit(f"sub {dest}, {right_operand}")
            elif stmt.op == "MUL":
                self.emit(f"imul {dest}, {right_operand}")
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

    def generate_move(self, stmt: Move):
        """Generate MOVE instruction: move value between registers or memory"""
        dest = self.get_register(stmt.dest)
        src = stmt.src

        # If src is a register, just move it directly
        if self.is_register(src):
            self.emit(f"mov {dest}, {self.get_register(src)}")
        else:
            # For memory or immediate values, move through a temporary register
            temp_reg = "r10"  # Use r10 as a temporary register
            if isinstance(src, int):
                self.emit(f"mov {temp_reg}, {src}")
            else:
                self.emit(f"mov {temp_reg}, [{src}]")
            self.emit(f"mov {dest}, {temp_reg}")

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

    def generate_function(self, stmt: Function):
        """Generate function definition"""
        self.emit_label(f"{stmt.name}")
        for s in stmt.body:
            self.generate_statement(s)

    def generate_call(self, stmt: Call):
        """Generate function call"""
        self.emit(f"call {stmt.name}")

    def generate_return(self, stmt: Return):
        """Generate return statement"""
        if stmt.value:
            # For now, assume value is a register, move to rax
            if self.is_register(stmt.value):
                self.emit(f"mov rax, {self.get_register(stmt.value)}")
        self.emit("ret")

    def generate_if(self, stmt: If):
        """Generate if-else-endif statement"""
        else_label = f"else_{self.label_counter}"
        endif_label = f"endif_{self.label_counter}"
        self.label_counter += 1

        self.generate_condition(stmt.condition, else_label)

        for s in stmt.then_body:
            self.generate_statement(s)

        if stmt.else_body:
            self.emit(f"jmp {endif_label}")
            self.emit_label(else_label)
            for s in stmt.else_body:
                self.generate_statement(s)
            self.emit_label(endif_label)
        else:
            self.emit_label(else_label)

    def generate_condition(self, cond: Condition, false_label: str):
        """Generate condition evaluation and jump to false_label if condition is false"""
        # Load left into r10
        if isinstance(cond.left, int):
            self.emit(f"mov r10, {cond.left}")
        elif self.is_register(cond.left):
            self.emit(f"mov r10, {self.get_register(cond.left)}")
        else:
            self.emit(f"mov r10, [{cond.left}]")

        # Load right into r11
        if isinstance(cond.right, int):
            self.emit(f"mov r11, {cond.right}")
        elif self.is_register(cond.right):
            self.emit(f"mov r11, {self.get_register(cond.right)}")
        else:
            self.emit(f"mov r11, [{cond.right}]")

        # Compare
        self.emit("cmp r10, r11")

        # Jump based on op
        if cond.op == "==":
            self.emit(f"jne {false_label}")
        elif cond.op == "!=":
            self.emit(f"je {false_label}")
        elif cond.op == ">":
            self.emit(f"jle {false_label}")
        elif cond.op == "<":
            self.emit(f"jge {false_label}")
        elif cond.op == ">=":
            self.emit(f"jl {false_label}")
        elif cond.op == "<=":
            self.emit(f"jg {false_label}")

    def generate_loop(self, stmt: Loop):
        """Generate LOOP var, limit / ENDLOOP - loop while var < limit"""
        start_label = f"loop_start_{self.label_counter}"
        end_label = f"loop_end_{self.label_counter}"
        self.label_counter += 1

        # Initialize var to 0
        self.emit(f"mov qword [{stmt.var}], 0")

        self.emit_label(start_label)

        # Compare var < limit
        self.emit(f"mov r10, [{stmt.var}]")
        self.emit(f"mov r11, {stmt.limit}")
        self.emit("cmp r10, r11")
        self.emit(f"jge {end_label}")

        # Body
        for s in stmt.body:
            self.generate_statement(s)

        # Increment var
        self.emit(f"inc qword [{stmt.var}]")
        self.emit(f"jmp {start_label}")

        self.emit_label(end_label)

    def generate_while(self, stmt: While):
        """Generate WHILE condition / ENDWHILE - loop while condition is true"""
        start_label = f"while_start_{self.label_counter}"
        end_label = f"while_end_{self.label_counter}"
        self.label_counter += 1

        self.emit_label(start_label)

        self.generate_condition(stmt.condition, end_label)

        # Body
        for s in stmt.body:
            self.generate_statement(s)

        self.emit(f"jmp {start_label}")

        self.emit_label(end_label)

    def generate_for(self, stmt: For):
        """Generate FOR var FROM start TO end [STEP step] / ENDFOR - range loop"""
        # Declare the variable if not already declared
        if stmt.var not in self.variables:
            self.variables[stmt.var] = True
            self.emit_bss(f"{stmt.var} resq 1")

        start_label = f"for_start_{self.label_counter}"
        end_label = f"for_end_{self.label_counter}"
        self.label_counter += 1

        # Initialize var to start
        self.emit(f"mov qword [{stmt.var}], {stmt.start}")

        self.emit_label(start_label)

        # Compare var > end (assuming step > 0)
        self.emit(f"mov r10, [{stmt.var}]")
        self.emit(f"mov r11, {stmt.end}")
        self.emit("cmp r10, r11")
        self.emit(f"jg {end_label}")

        # Body
        for s in stmt.body:
            self.generate_statement(s)

        # Increment var by step
        if stmt.step == 1:
            self.emit(f"inc qword [{stmt.var}]")
        else:
            self.emit(f"add qword [{stmt.var}], {stmt.step}")

        self.emit(f"jmp {start_label}")

        self.emit_label(end_label)

    def generate_repeat(self, stmt: Repeat):
        """Generate REPEAT / UNTIL condition - post-condition loop"""
        start_label = f"repeat_start_{self.label_counter}"
        self.label_counter += 1

        self.emit_label(start_label)

        # Body
        for s in stmt.body:
            self.generate_statement(s)

        # Condition - if false, jump back
        self.generate_condition(stmt.condition, start_label)

