from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SearchPlan:
    queries: tuple[str, ...]
    page_size: int = 20
    max_pages: int = 3
    max_candidates: int = 100
    destination_country: str = "CA"
    required_currency: str = "USD"
    filters: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.queries:
            raise ValueError("Le plan doit contenir au moins une requête.")
        if not 1 <= self.page_size <= 100:
            raise ValueError("page_size hors limites")
        if not 1 <= self.max_pages <= 20:
            raise ValueError("max_pages hors limites")
