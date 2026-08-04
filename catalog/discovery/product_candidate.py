from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ProductCandidate:
    source_id: str
    title: str
    supplier_id: str = ""
    category_id: str = ""
    currency: str = "USD"
    unit_cost: float = 0.0
    min_order_quantity: int = 1
    image_urls: tuple[str, ...] = ()
    signals: dict[str, float] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
