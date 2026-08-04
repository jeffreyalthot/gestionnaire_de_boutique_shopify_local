from __future__ import annotations

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True, slots=True)
class FixedLine:
    key: str
    row: int
    width: int


class FixedLineRegistry:
    def __init__(self, width: int = 100) -> None:
        self.width = max(40, width)
        self._lock = RLock()
        self._lines: dict[str, FixedLine] = {}

    def register(self, key: str, row: int, width: int | None = None) -> FixedLine:
        with self._lock:
            if key in self._lines or any(line.row == row for line in self._lines.values()):
                raise ValueError(f"Ligne fixe déjà réservée: {key}/{row}")
            line = FixedLine(key, row, width or self.width)
            self._lines[key] = line
            return line

    def get(self, key: str) -> FixedLine:
        return self._lines[key]

    def rows(self) -> tuple[FixedLine, ...]:
        return tuple(sorted(self._lines.values(), key=lambda item: item.row))
