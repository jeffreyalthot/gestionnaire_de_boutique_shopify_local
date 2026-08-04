from __future__ import annotations

from decimal import Decimal

from domain.value_objects.idempotency_key import build_idempotency_key


class PurchaseOrderBuilder:
    def build(self, supplier_id: str, items: list[dict[str, object]], address: dict[str, object],
              batch_id: str, shopify_order_id: str) -> dict[str, object]:
        supplier_id = str(supplier_id).strip()
        if not supplier_id: raise ValueError("supplier_id requis")
        if not items: raise ValueError("Une commande fournisseur doit contenir des articles.")
        normalized = []
        total = Decimal("0")
        for index, item in enumerate(items):
            quantity = int(item.get("quantity", 0) or 0)
            sku = str(item.get("supplier_sku_id", item.get("sku", ""))).strip()
            if quantity <= 0 or not sku: raise ValueError(f"article fournisseur invalide: {index}")
            price = Decimal(str(item.get("unit_cost", item.get("unit_supplier_cost_cad", 0)) or 0))
            normalized.append({**item, "quantity": quantity, "supplier_sku_id": sku, "unit_cost": price})
            total += price * quantity
        required_address = ("address1", "city", "country_code", "postal_code")
        missing = [key for key in required_address if not address.get(key)]
        if missing: raise ValueError("adresse fournisseur incomplète: " + ",".join(missing))
        return {
            "supplier_id": supplier_id, "items": normalized, "address": dict(address),
            "remark": f"Shopify order {shopify_order_id}; batch {batch_id}"[:500],
            "estimated_total": total,
            "idempotency_key": build_idempotency_key("alibaba-order", batch_id, supplier_id, shopify_order_id),
        }
