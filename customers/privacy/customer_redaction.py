from __future__ import annotations

from typing import Any


class CustomerRedaction:
    def __init__(self, db: Any) -> None:
        self.db = db

    def redact(self, customer_id: str) -> dict[str, int]:
        profile = self.db.execute(
            "UPDATE customer_profiles SET email_hash='',country_code='',language='',preferences_json='{}',tags_json='[]',updated_at=datetime('now') WHERE customer_id=?",
            (customer_id,),
        )
        orders = self.db.execute("UPDATE orders SET customer_id='',encrypted_shipping_address='' WHERE customer_id=?", (customer_id,))
        tickets = self.db.execute("UPDATE customer_tickets SET customer_id='',body_encrypted='' WHERE customer_id=?", (customer_id,))
        memberships = self.db.execute("DELETE FROM customer_segment_memberships WHERE customer_id=?", (customer_id,))
        self.db.insert_audit("customer.redacted", "privacy-service", {"customer_id": customer_id, "profile": profile, "orders": orders, "tickets": tickets})
        return {"profile": profile, "orders": orders, "tickets": tickets, "segments": memberships}
