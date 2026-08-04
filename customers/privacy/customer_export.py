from __future__ import annotations

from typing import Any


class CustomerExport:
    def __init__(self, db: Any) -> None:
        self.db = db

    def build(self, customer_id: str) -> dict[str, Any]:
        profile = self.db.query_one("SELECT * FROM customer_profiles WHERE customer_id=?", (customer_id,))
        consents = self.db.query("SELECT purpose,granted,source,recorded_at,expires_at FROM customer_consents WHERE customer_id=? ORDER BY recorded_at", (customer_id,))
        orders = self.db.query("SELECT id,name,currency,total_amount,financial_status,fulfillment_status,created_at FROM orders WHERE customer_id=? ORDER BY created_at", (customer_id,))
        tickets = self.db.query("SELECT id,order_id,category,status,subject,created_at,updated_at FROM customer_tickets WHERE customer_id=? ORDER BY created_at", (customer_id,))
        return {"customer_id": customer_id, "profile": profile, "consents": consents, "orders": orders, "tickets": tickets}
