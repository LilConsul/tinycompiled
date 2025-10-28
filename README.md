# [WIP] TinyCompiled

**A Small Educational Compiler and Visualizer for Assembly Language Learning**

Authors: Denys Shevchenko, Yehor Karabanov

TinyCompiled is a small educational compiler and visualizer for a custom assembly-like language designed to help new developers understand the fundamentals of low-level programming, assembly language, and compilation. The project focuses on demonstrating how high-level instructions are translated into assembly code, providing an intuitive and interactive experience for learning and experimentation.

## Overview

TinyCompiled takes programs written in **TinyCompiled** (`.tc` files) — a simplified, human-readable assembly-like language — and translates them into real **x86-64 NASM assembly**, allowing users to see exactly how each instruction maps to low-level operations. By combining compilation with visualization, TinyCompiled bridges the gap between abstract programming concepts and the underlying machine instructions, making it a powerful tool for students, educators, and hobbyists.

## Key Features

### 🔄 TinyCompiled (.tc) → NASM Translation
TinyCompiled converts TinyCompiled instructions into NASM assembly line by line, including:
- Arithmetic operations
- Data movement
- Control flow
- Input/output instructions

Each translation preserves the logical structure of the program, making it easy to follow and understand how high-level logic is implemented in assembly.

### 📊 Side-by-Side Visualization
Using the **Textualize/Textual** Python library, TinyCompiled displays TinyCompiled code alongside its NASM translation in a diff-style table. This visualization allows users to clearly see the mapping between abstract instructions and real machine operations, highlighting the effect of each line in an interactive terminal interface.

### 💻 CLI Interface
The command-line interface provides simple commands for:
- Translating programs
- Viewing translations
- Exporting programs

This makes TinyCompiled easy to use in a variety of environments and workflows.

### 📝 String Handling (Optional)
TinyCompiled supports basic string instructions, including:
- Loading literals
- Printing
- Concatenation
- Optional string-to-number conversions

This demonstrates how textual data is stored and manipulated at a low level, helping beginners grasp how memory and registers interact with strings.

## Example

### TinyCompiled (.tc) File

```assembly
LOAD R1, 5
LOAD R2, 10
ADD R3, R1, R2
PRINT R3
HALT
```

## Project Goals

- **Educational Focus**: Help beginners understand assembly language and low-level programming concepts
- **Interactive Learning**: Provide real-time visualization of code translation
- **Accessibility**: Make assembly language learning approachable and engaging
- **Practical Knowledge**: Bridge the gap between high-level and low-level programming

## Getting Started
[WIP]

## License

This project is provided for educational purposes. Please refer to the repository for specific licensing information.

## References

- [GitHub Repository](https://github.com/LilConsul/tinycompiled)
- x86-64 Assembly Language Resources
- NASM Assembler Documentation

