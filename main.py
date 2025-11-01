from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import TextArea, Static
from textual.reactive import var

from src import compile_tc_to_nasm


def translate_tc_to_nasm(tc_code: str) -> str:
    return tc_code


class TinyCompiledApp(App):
    tc_code = var("")

    def compose(self) -> ComposeResult:
        self.editor = TextArea(
            placeholder="Write TinyCompiled code here...",
            language="python",
            show_line_numbers=True,
            soft_wrap=False,
            tab_behavior="indent",
        )
        self.output = Static("NASM translation will appear here.", expand=True)
        yield Horizontal(self.editor, self.output)

    def on_mount(self) -> None:
        # Soft lavender background
        self.screen.styles.background = "#2d1b4e"

        # Container styling
        horizontal = self.query_one(Horizontal)
        horizontal.styles.height = "100%"
        horizontal.styles.background = "#2d1b4e"

        # Editor - soft purple with rounded border
        self.editor.styles.width = "1fr"
        self.editor.styles.height = "100%"
        self.editor.styles.border = ("round", "#b794f6")
        self.editor.styles.background = "#3d2b5f"
        self.editor.styles.padding = (1, 2)

        # Output - lighter soft purple with accent border
        self.output.styles.width = "1fr"
        self.output.styles.height = "100%"
        self.output.styles.border = ("round", "#d4b5ff")
        self.output.styles.background = "#4a3470"
        self.output.styles.color = "#f0e6ff"
        self.output.styles.padding = (2, 3)
        self.output.styles.overflow_y = "auto"

        self.editor.focus()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.tc_code = event.text_area.text
        nasm_code = translate_tc_to_nasm(self.tc_code)
        self.output.update(nasm_code)


if __name__ == "__main__":
    # TinyCompiledApp().run()

    # Example 1: Comprehensive tests
    example1 = """
 ; Test FUNC, CALL, RET - Simple function
FUNC myfunc
LOAD R1, 42
RET
ENDFUNC

CALL myfunc
PRINT R1

 ; Test RET with register
FUNC add_one
LOAD R1, 5
ADD R1, R1, 1
RET R1
ENDFUNC

CALL add_one
PRINT R1

 ; Test function calling another
FUNC inner
LOAD R2, 10
RET R2
ENDFUNC

FUNC outer
CALL inner
ADD R1, R2, 5
RET R1
ENDFUNC

CALL outer
PRINT R1

 ; Test with variables
VAR x
FUNC set_x
LOAD R1, 100
SET x, R1
RET
ENDFUNC

CALL set_x
LOAD R1, x
PRINT R1

 ; Test nested calls
FUNC func_a
LOAD R1, 1
RET R1
ENDFUNC

FUNC func_b
CALL func_a
ADD R2, R1, 2
RET R2
ENDFUNC

CALL func_b
PRINT R2

 ; Test IF ELSE ENDIF
LOAD R1, 10
IF R1 == 10
LOAD R2, 20
PRINT R2
ELSE
LOAD R2, 30
PRINT R2
ENDIF

LOAD R1, 5
IF R1 != 10
LOAD R2, 40
PRINT R2
ELSE
LOAD R2, 50
PRINT R2
ENDIF

HALT
    """

    print("Compiling TinyCompiled to NASM...")
    print("=" * 60)
    asm_output = compile_tc_to_nasm(example1)
    print(asm_output)
    print("=" * 60)
    print("\nTo assemble and run:")
    # print("nasm -f elf64 -o test.o <YOUR_FILENAME>.asm && ld test.o -o test && ./test && rm test.o test")
    print(
        "nasm -f elf64 -o test.o test_.asm && ld test.o -o test && ./test && rm test.o test"
    )
    with open("./test_output/test_.asm", "w") as f:
        f.write(asm_output)
