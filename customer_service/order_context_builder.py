from __future__ import annotations

from typing import Any


class OrderContextBuilder:
    def __init__(self, db: Any) -> None:
        self.db = db

    def build(self, order_id: str) -> dict[str, Any]:
        order = self.db.query_one(
            "SELECT id,name,currency,total_amount,financial_status,fulfillment_status,procurement_status,risk_level,created_at,updated_at FROM orders WHERE id=? OR shopify_order_id=?",
            (order_id, order_id),
        )
        if not order:
            return {"found": False, "order_id": order_id}
        lines = self.db.query("SELECT sku,title,quantity,status FROM order_lines WHERE order_id=? ORDER BY id", (order["id"],))
        shipments = self.db.query("SELECT carrier,tracking_number,tracking_url,status,updated_at FROM shipments WHERE order_id=? ORDER BY updated_at DESC", (order["id"],))
        return {"found": True, "order": order, "lines": lines, "shipments": shipments}
