from cli.menu_renderer import MenuRenderer
from cli.main_menu import OPTIONS
class InteractiveShell:
    def __init__(self) -> None: self.renderer=MenuRenderer()
    def display(self) -> None: self.renderer.show("Commerce Orchestrator",OPTIONS)
