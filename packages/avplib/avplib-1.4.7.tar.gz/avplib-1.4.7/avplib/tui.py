import os
from textual.app import App, ComposeResult  
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Header, Footer, Button, Label, LoadingIndicator
from textual.layouts.grid import GridLayout

# ! Types


# ! Screens
class CAVScreen(Screen):
    TITLE = "avplib.tui"
    SUB_TITLE = "CAV"
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with GridLayout():
            ...
        yield Label("", classes="label-one-line")
        yield Label("", classes="label-full-screen")
        yield Footer()

class ConvertScreen(Screen):
    TITLE = "avplib.tui"
    SUB_TITLE = "Convert"
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

class PlayScreen(Screen):
    TITLE = "avplib.tui"
    SUB_TITLE = "Play"
    BINDINGS = [Binding("escape", "app.pop_screen", "Back")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

# ! Text Constants
SELECTE_MODE_TEXT = \
"""\
███ ███ █   ███ ████ ███    █   █ ████ ████  ███
█   █   █   █   █  █  █     ██ ██ █  █ █  ██ █  
███ ███ █   ███ █     █     █ █ █ █  █ █  ██ ███
  █ █   █   █   █  █  █     █   █ █  █ █  ██ █  
███ ███ ███ ███ ████  █     █   █ ████ ████  ███
"""

# ! Main App
class AVPLibApp(App):
    CSS_PATH = os.path.join(os.path.dirname(__file__), "tui.css")
    TITLE = "avplib.tui"
    SUB_TITLE = "Main"
    
    def on_mount(self):
        self.install_screen(CAVScreen(), name="cav")
        self.install_screen(ConvertScreen(), name="convert")
        self.install_screen(PlayScreen(), name="play")
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(SELECTE_MODE_TEXT, classes="mode-label")
        yield Button("🔱 [b]CAV[/] 🔱", id="ms_cav", classes="mode-button")
        yield Button("♻ [b]CONVERT[/] ♻", id="ms_convert", classes="mode-button")
        yield Button("⏯ [b]PLAY[/] ⏯", id="ms_play", classes="mode-button")
        yield Footer()
    
    def pop_screen(self) -> Screen:
        self.sub_title = "Main"
        return super().pop_screen()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ms_cav":
            self.sub_title = "CAV"
            await self.push_screen('cav')
        elif event.button.id == "ms_convert":
            self.sub_title = "Convert"
            await self.push_screen('convert')
        elif event.button.id == "ms_play":
            self.sub_title = "Play"
            await self.push_screen('play')

# ! Start
if __name__ == "__main__":
    app = AVPLibApp()
    app.run()