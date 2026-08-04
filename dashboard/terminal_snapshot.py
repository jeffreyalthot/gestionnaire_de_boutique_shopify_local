from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class TerminalSnapshot:
    page: str
    lines: tuple[str, ...]
    state: dict[str, Any]
