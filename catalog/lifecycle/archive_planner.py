from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ArchivePlan:
    product_id: str
    action: str
    preserve_redirect: bool
    preserve_analytics: bool
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ArchivePlanner:
    def plan(self, product: dict[str, object]) -> ArchivePlan:
        product_id = str(product.get("id", ""))
        sales_90d = int(product.get("sales_90d", 0) or 0)
        stock = int(product.get("stock", 0) or 0)
        supplier_active = bool(product.get("supplier_active", True))
        if not supplier_active and stock <= 0:
            return ArchivePlan(product_id, "archive", True, True, "supplier_delisted_and_no_stock")
        if sales_90d <= 0 and stock <= 0:
            return ArchivePlan(product_id, "archive", True, True, "no_sales_no_stock")
        return ArchivePlan(product_id, "keep", False, True, "still_viable")
