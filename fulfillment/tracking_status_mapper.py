from __future__ import annotations


class TrackingStatusMapper:
    MAP = {
        "pending": "pending", "info_received": "label_created", "accepted": "in_transit",
        "pickup": "in_transit", "in_transit": "in_transit", "out_for_delivery": "out_for_delivery",
        "delivered": "delivered", "exception": "exception", "failed_attempt": "delivery_attempted",
        "expired": "lost", "undeliverable": "undeliverable", "returned": "returned",
    }

    def map(self, source_status: str) -> str:
        return self.MAP.get(source_status.strip().casefold().replace(" ", "_"), "unknown")
