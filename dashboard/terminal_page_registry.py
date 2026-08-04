from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

RenderFunction = Callable[[dict[str, object]], list[str]]


@dataclass(frozen=True, slots=True)
class TerminalPage:
    key: str
    title: str
    render: RenderFunction


class TerminalPageRegistry:
    def __init__(self) -> None:
        self._pages: dict[str, TerminalPage] = {}
        self._order: list[str] = []

    def register(self, page: TerminalPage) -> None:
        if page.key in self._pages:
            raise ValueError(page.key)
        self._pages[page.key] = page
        self._order.append(page.key)

    def page(self, key: str) -> TerminalPage:
        return self._pages[key]

    def keys(self) -> tuple[str, ...]:
        return tuple(self._order)
