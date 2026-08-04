from __future__ import annotations


class SupplierDelistingHandler:
    def plan(self, products: list[dict[str, object]]) -> tuple[dict[str, object], ...]:
        plans = []
        for product in products:
            stock = int(product.get("stock", 0) or 0)
            action = "unpublish" if stock <= 0 else "freeze_supplier_sync"
            plans.append({"product_id": str(product.get("id", "")), "action": action,
                          "preserve_orders": True, "reason": "supplier_delisted"})
        return tuple(plans)
