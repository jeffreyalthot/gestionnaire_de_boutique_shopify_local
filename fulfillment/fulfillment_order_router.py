from __future__ import annotations

from collections import defaultdict

from fulfillment.fulfillment_plan import FulfillmentPlan


class FulfillmentOrderRouter:
    def route(self, order_id: str, lines: list[dict[str, object]]) -> FulfillmentPlan:
        by_supplier: dict[str, list[dict[str, object]]] = defaultdict(list)
        for line in lines:
            supplier = str(line.get("supplier_id", ""))
            if not supplier: raise ValueError(f"Fournisseur absent pour la ligne {line.get('id','')}")
            by_supplier[supplier].append(line)
        shipments=[]
        for supplier, supplier_lines in sorted(by_supplier.items()):
            shipments.append({"supplier_id": supplier, "line_ids": tuple(str(line.get("id", "")) for line in supplier_lines),
                              "status": "awaiting_supplier_order"})
        return FulfillmentPlan(order_id, tuple(sorted(by_supplier)), tuple(shipments))
