from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class DeliveryExceptionDecision:
    shipment_id: str
    category: str
    severity: str
    action: str
    customer_notification: bool
    supplier_escalation: bool
    recorded_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DeliveryExceptionHandler:
    CATEGORIES = {
        "lost": ("critical", "open_carrier_claim", True, True),
        "damaged": ("high", "request_evidence", True, True),
        "customs": ("high", "resolve_customs", True, True),
        "address": ("medium", "request_address_confirmation", True, False),
        "refused": ("medium", "start_return_to_sender", True, False),
        "delay": ("low", "monitor", True, False),
    }

    def __init__(self, db: Database) -> None:
        self.db = db

    def handle(self, shipment_id: str, reason: str, *, details: dict[str, object] | None = None) -> DeliveryExceptionDecision:
        category = self.classify(reason)
        severity, action, notify, escalate = self.CATEGORIES[category]
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute("UPDATE shipments SET status='exception', updated_at=? WHERE id=?", (now, shipment_id))
        decision = DeliveryExceptionDecision(shipment_id, category, severity, action, notify, escalate, now)
        self.db.insert_audit("delivery_exception", "system", {**decision.as_dict(), "reason": reason, "details": details or {}})
        return decision

    @classmethod
    def classify(cls, reason: str) -> str:
        value = str(reason).lower()
        aliases = {
            "lost": ("lost", "missing", "introuvable"),
            "damaged": ("damaged", "broken", "endommag"),
            "customs": ("customs", "douane", "clearance"),
            "address": ("address", "adresse", "incorrect"),
            "refused": ("refused", "refus", "return to sender"),
        }
        return next((category for category, words in aliases.items() if any(word in value for word in words)), "delay")


def record_delivery_exception(db: Database, shipment_id: str, reason: str) -> None:
    DeliveryExceptionHandler(db).handle(shipment_id, reason)
