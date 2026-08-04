from rich.console import Console
class TerminalNotifier:
    def __init__(self) -> None: self.console=Console(stderr=True)
    def info(self,message: str) -> None: self.console.print(f"[cyan]INFO[/cyan] {message}")
    def warning(self,message: str) -> None: self.console.print(f"[yellow]ATTENTION[/yellow] {message}")
    def critical(self,message: str) -> None: self.console.print(f"[bold red]CRITIQUE[/bold red] {message}")
