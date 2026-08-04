from __future__ import annotations

import hashlib
import json


class OrderDeduplicator:
    @staticmethod
    def fingerprint(order: dict[str, object]) -> str:
        stable = {
            "external_id": order.get("id") or order.get("shopify_order_id"),
            "customer": order.get("customer_id"),
            "created_at": order.get("created_at"),
            "total": order.get("total_amount") or order.get("total"),
            "lines": order.get("lines", []),
        }
        material = json.dumps(stable, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(material.encode()).hexdigest()

    def is_duplicate(self, order: dict[str, object], known: set[str]) -> bool:
        return self.fingerprint(order) in known
