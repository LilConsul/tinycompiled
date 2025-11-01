from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import TextArea, Static, Footer, Button, Label, Input
from textual.reactive import var
from textual.screen import ModalScreen
from pathlib import Path

from src import compile_tc_to_nasm


class SaveDialog(ModalScreen[tuple[str, str]]):
    """Modal dialog for saving files."""

    def __init__(self, tc_code: str, asm_code: str):
        super().__init__()
        self.tc_code = tc_code
        self.asm_code = asm_code

    def compose(self) -> ComposeResult:
        with Container(id="save-dialog"):
            yield Label("Save File", id="dialog-title")
            yield Label("Choose file type and enter filename:")
            yield Input(placeholder="filename (without extension)", id="filename-input")
            with Horizontal(id="button-container"):
                yield Button("Save .tc", variant="primary", id="save-tc")
                yield Button("Save .asm", variant="success", id="save-asm")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        else:
            filename_input = self.query_one("#filename-input", Input)
            filename = filename_input.value.strip()

            if not filename:
                return

            if event.button.id == "save-tc":
                filepath = f"{filename}.tc"
                content = self.tc_code
            else:  # save-asm
                filepath = f"{filename}.asm"
                content = self.asm_code

            self.dismiss((filepath, content))


class TinyCompiledApp(App):
    CSS_PATH = "src/main.css"
    BINDINGS = [
        ("ctrl+r", "recompile", "Recompile"),
        ("ctrl+s", "save", "Save File"),
    ]

    tc_code = var("")
    nasm_code = var("")

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
        yield Footer()

    def on_mount(self) -> None:
        self.editor.focus()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.tc_code = event.text_area.text
        # self.nasm_code = compile_tc_to_nasm(self.tc_code)
        # self.output.update(self.nasm_code)

    def action_recompile(self) -> None:
        """Recompile the current code."""
        try:
            self.nasm_code = compile_tc_to_nasm(self.tc_code)
        except Exception as e:
            self.nasm_code = f"Error during compilation:\n{e}"
        self.output.update(self.nasm_code)

    async def action_save(self) -> None:
        """Open save dialog."""
        result = await self.push_screen_wait(SaveDialog(self.tc_code, self.nasm_code))
        if result:
            filepath, content = result
            try:
                Path(filepath).write_text(content, encoding="utf-8")
                self.notify(f"Saved to {filepath}", severity="information")
            except Exception as e:
                self.notify(f"Error saving file: {e}", severity="error")


if __name__ == "__main__":
    TinyCompiledApp().run()
    