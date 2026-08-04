from rich.console import Console
from rich.table import Table
class MenuRenderer:
    def __init__(self) -> None: self.console=Console()
    def show(self,title: str,options: list[tuple[str,str]]) -> None:
        table=Table(title=title); table.add_column("#"); table.add_column("Action")
        for key,label in options: table.add_row(key,label)
        self.console.print(table)
