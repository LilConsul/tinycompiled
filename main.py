from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Container, Vertical
from textual.widgets import (
    TextArea,
    Footer,
    Button,
    Label,
    Input,
    DirectoryTree,
)
from textual.reactive import var
from textual.screen import ModalScreen
from pathlib import Path

from src import compile_tc_to_nasm


class SaveDialog(ModalScreen[tuple[str, str]]):
    """Modal dialog for saving files with directory browser."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("up", "parent_dir", "Go Up"),
    ]

    def __init__(self, tc_code: str, asm_code: str):
        super().__init__()
        self.tc_code = tc_code
        self.asm_code = asm_code
        self.selected_dir = Path.cwd()

    def compose(self) -> ComposeResult:
        with Container(id="save-dialog"):
            yield Label("Save File", id="dialog-title")

            with Vertical(id="dialog-content"):
                yield Label("📁 Select directory (↑ to go up):", id="dir-label")
                yield DirectoryTree(str(self.selected_dir), id="dir-tree")

                yield Label(
                    f"Current: {self.selected_dir.absolute()}", id="current-dir"
                )

                yield Input(
                    placeholder="filename.tc or filename.asm",
                    id="filename-input",
                    value="output.asm",
                )

            with Horizontal(id="button-container"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        """Focus the filename input when dialog opens."""
        self.query_one("#filename-input", Input).focus()

    def action_parent_dir(self) -> None:
        """Navigate to parent directory."""
        parent = self.selected_dir.parent
        if parent != self.selected_dir:  # Not at root
            self.selected_dir = parent
            self.refresh_directory_tree()

    def refresh_directory_tree(self) -> None:
        """Refresh the directory tree with the new directory."""
        tree = self.query_one("#dir-tree", DirectoryTree)
        tree.path = str(self.selected_dir)
        tree.reload()
        current_dir_label = self.query_one("#current-dir", Label)
        current_dir_label.update(f"Current: {self.selected_dir.absolute()}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Save file when Enter is pressed in the filename input."""
        if event.input.id == "filename-input":
            self.save_file()

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        """Update selected directory when user clicks on a directory."""
        self.selected_dir = event.path
        current_dir_label = self.query_one("#current-dir", Label)
        current_dir_label.update(f"Current: {self.selected_dir.absolute()}")

    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(None)

    def save_file(self) -> None:
        """Save file with auto-detection of type based on extension."""
        filename_input = self.query_one("#filename-input", Input)
        filename = filename_input.value.strip()

        if not filename:
            self.notify("⚠️ Please enter a filename", severity="warning")
            return

        # Auto-detect file type from extension
        if filename.endswith(".tc"):
            filepath = self.selected_dir / filename
            content = self.tc_code
            file_type = "TinyCompiled source"
            if not content.strip():
                self.notify("⚠️ No TC code to save", severity="warning")
                return
        elif filename.endswith(".asm"):
            filepath = self.selected_dir / filename
            content = self.asm_code
            file_type = "NASM assembly"
            if not content.strip():
                self.notify(
                    "⚠️ No compiled ASM code to save. Press Ctrl+R to compile first.",
                    severity="warning",
                )
                return
        else:
            self.notify("⚠️ Please specify .tc or .asm extension", severity="warning")
            return

        if filepath.exists():
            self.notify(
                f"⚠️ File {filepath.name} already exists - overwriting",
                severity="warning",
            )

        self.notify(f"💾 Saving {file_type} to {filepath.name}...", severity="information")
        self.dismiss((str(filepath), content))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.action_cancel()
        elif event.button.id == "save":
            self.save_file()


class TinyCompiledApp(App):
    CSS_PATH = "src/main.tcss"
    BINDINGS = [
        Binding("ctrl+r", "recompile", "Recompile", show=True),
        Binding("ctrl+s", "save", "Save File", show=True, priority=True),
    ]

    tc_code = var("")
    nasm_code = var("")

    def compose(self) -> ComposeResult:
        self.editor = TextArea(
            placeholder="Write TinyCompiled code here...",
            show_line_numbers=True,
            soft_wrap=False,
            tab_behavior="indent",
        )
        self.output = TextArea(
            "NASM translation will appear here.",
            read_only=True,
            show_line_numbers=True,
            soft_wrap=False,
            tab_behavior="indent",
        )
        yield Horizontal(self.editor, self.output)
        yield Footer()

    def on_mount(self) -> None:
        self.editor.focus()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area == self.editor:
            self.tc_code = event.text_area.text

    def action_recompile(self) -> None:
        """Recompile the current code."""
        try:
            self.nasm_code = compile_tc_to_nasm(self.tc_code)
        except Exception as e:
            self.nasm_code = f"Error during compilation:\n{e}"
        self.output.load_text(self.nasm_code)

    def action_save(self) -> None:
        """Open save dialog."""

        def handle_save_result(result: tuple[str, str] | None) -> None:
            if result:
                filepath, content = result
                try:
                    Path(filepath).write_text(content, encoding="utf-8")
                    self.notify(f"Saved to {filepath}", severity="information")
                except Exception as e:
                    self.notify(f"Error saving file: {e}", severity="error")

        self.push_screen(SaveDialog(self.tc_code, self.nasm_code), handle_save_result)


if __name__ == "__main__":
    TinyCompiledApp().run()
    