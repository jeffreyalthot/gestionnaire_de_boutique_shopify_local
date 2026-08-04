from __future__ import annotations

from collections import defaultdict


class SupplierLineMapper:
    def group(self, lines: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for line in lines:
            supplier_id = str(line.get("supplier_id") or line.get("supplierId") or "")
            product_id = str(line.get("supplier_product_id") or "")
            sku_id = str(line.get("supplier_sku_id") or "")
            quantity = int(line.get("quantity", 0) or 0)
            if not supplier_id or not product_id or quantity <= 0:
                raise ValueError("Ligne fournisseur incomplète")
            grouped[supplier_id].append({**line, "supplier_id": supplier_id, "supplier_product_id": product_id, "supplier_sku_id": sku_id, "quantity": quantity})
        return dict(grouped)
