from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class InventoryReconciliation:
    shopify: int
    supplier: int
    safety_stock: int
    reserved: int
    desired: int
    delta: int
    change_required: bool
    severity: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class InventoryReconciler:
    def compare(self, shopify_stock: int, supplier_stock: int, safety_stock: int,
                reserved: int = 0) -> dict[str, int | bool | str]:
        return self.reconcile(shopify_stock, supplier_stock, safety_stock, reserved).as_dict()

    def reconcile(self, shopify_stock: int, supplier_stock: int, safety_stock: int,
                  reserved: int = 0) -> InventoryReconciliation:
        desired = max(0, int(supplier_stock) - max(0, int(safety_stock)) - max(0, int(reserved)))
        delta = desired - int(shopify_stock)
        ratio = abs(delta) / max(1, desired, int(shopify_stock))
        severity = "critical" if ratio >= .5 else ("high" if ratio >= .2 else ("medium" if ratio >= .05 else "none"))
        return InventoryReconciliation(int(shopify_stock), int(supplier_stock), int(safety_stock), int(reserved), desired, delta, delta != 0, severity)
