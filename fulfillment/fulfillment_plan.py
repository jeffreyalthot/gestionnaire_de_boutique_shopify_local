from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class FulfillmentPlan:
    order_id: str
    supplier_orders: tuple[str, ...]
    shipments: tuple[dict[str, Any], ...]
    status: str = "planned"
    id: str = field(default_factory=lambda: str(uuid4()))

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
