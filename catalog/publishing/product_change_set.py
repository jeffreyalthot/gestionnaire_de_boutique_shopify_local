from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ProductChangeSet:
    product_id: str
    create: bool = False
    fields: dict[str, Any] = field(default_factory=dict)
    variants: tuple[dict[str, Any], ...] = ()
    media: tuple[dict[str, Any], ...] = ()
    publications: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
