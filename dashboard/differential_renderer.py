from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinePatch:
    row: int
    text: str


class DifferentialRenderer:
    def __init__(self) -> None:
        self._previous: dict[int, str] = {}

    def diff(self, lines: dict[int, str], width: int) -> list[LinePatch]:
        patches: list[LinePatch] = []
        for row, value in sorted(lines.items()):
            text = self._fit(value, width)
            if self._previous.get(row) != text:
                patches.append(LinePatch(row, text))
                self._previous[row] = text
        return patches

    @staticmethod
    def _fit(value: str, width: int) -> str:
        safe = ''.join(character if 32 <= ord(character) < 127 or ord(character) >= 160 else '?' for character in value)
        if len(safe) > width:
            safe = safe[:max(0, width - 1)] + '…'
        return safe.ljust(width)

    def reset(self) -> None:
        self._previous.clear()
