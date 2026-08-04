from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SourceCursor:
    query_index: int = 0
    page: int = 1
    exhausted: bool = False

    def advance(self, *, max_pages: int, query_count: int) -> None:
        if self.exhausted:
            return
        self.page += 1
        if self.page > max_pages:
            self.query_index += 1
            self.page = 1
        if self.query_index >= query_count:
            self.exhausted = True
