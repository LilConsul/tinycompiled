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

    # Example 1: Simple arithmetic
    example1 = """
 ; Test INPUT, NOP, and HALT
VAR user_input
INPUT user_input    ; Read integer from stdin into user_input
NOP                 ; No operation (placeholder)
PRINT user_input    ; Print the input value
HALT                ; Terminate program
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
