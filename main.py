from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import Static, TextArea
from textual.reactive import var

from src import compile_tc_to_nasm


def translate_tc_to_nasm(tc_code: str) -> str:
    """Translate TinyCompiled code to NASM assembly."""
    if not tc_code or not tc_code.strip():
        return "NASM translation will appear here."

    try:
        nasm_output = compile_tc_to_nasm(tc_code)
        return nasm_output
    except Exception as e:
        return f"Error during compilation:\n{str(e)}"


class TinyCompiledApp(App):
    """TinyCompiled IDE with live syntax highlighting preview."""

    CSS = """
    #editor-container {
        width: 1fr;
        height: 100%;
    }
    
    #output-container {
        width: 1fr;
        height: 100%;
    }
    
    .panel-title {
        height: 1;
        background: #1d0b3e;
        color: #d4b5ff;
        padding: 0 2;
        text-align: center;
    }
    """

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

        with Horizontal():
            with Container(id="editor-container"):
                yield Static("TinyCompiled Editor", classes="panel-title")
                yield self.editor
            with Container(id="output-container"):
                yield Static("NASM Output", classes="panel-title")
                yield self.output

    def on_mount(self) -> None:
        # Soft lavender background
        self.screen.styles.background = "#2d1b4e"

        # Editor styling
        self.editor.styles.height = "1fr"
        self.editor.styles.border = ("round", "#b794f6")
        self.editor.styles.background = "#3d2b5f"
        self.editor.styles.padding = (1, 2)

        # Output styling
        self.output.styles.height = "1fr"
        self.output.styles.border = ("round", "#d4b5ff")
        self.output.styles.background = "#4a3470"
        self.output.styles.color = "#f0e6ff"
        self.output.styles.padding = (2, 3)
        self.output.styles.overflow_y = "auto"

        self.editor.focus()

    def on_text_area_changed(self, event) -> None:
        """Handle text changes - update NASM output."""
        self.tc_code = event.text_area.text

        # # Update NASM output
        # nasm_code = translate_tc_to_nasm(self.tc_code)
        # self.output.update(nasm_code)


if __name__ == "__main__":
    TinyCompiledApp().run()
