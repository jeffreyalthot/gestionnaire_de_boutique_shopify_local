from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

Renderer = Callable[[dict[str, Any], int], list[str]]


@dataclass(frozen=True)
class TerminalPageDefinition:
    key: str
    title: str
    renderer: Renderer
    minimum_width: int = 78

    def render(self, state: dict[str, Any], width: int, line_count: int) -> list[str]:
        lines = list(self.renderer(state, max(width, self.minimum_width)))[:line_count]
        lines.extend([''] * (line_count - len(lines)))
        return lines
