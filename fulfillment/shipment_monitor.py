from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from fulfillment.late_shipment_detector import LateShipmentDetector
from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class ShipmentMonitorSnapshot:
    active: int
    late: int
    exceptions: int
    by_status: dict[str, int]
    generated_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ShipmentMonitor:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.detector = LateShipmentDetector()

    def pending(self, limit: int = 100) -> list[dict[str, object]]:
        return self.db.query("SELECT * FROM shipments WHERE status NOT IN ('delivered','cancelled') ORDER BY updated_at LIMIT ?", (max(1, int(limit)),))

    def assess(self, *, maximum_days: int = 7, limit: int = 500) -> list[dict[str, object]]:
        result = []
        for shipment in self.pending(limit):
            assessment = self.detector.assess(str(shipment.get("updated_at") or datetime.now(timezone.utc).isoformat()), maximum_days)
            result.append({**shipment, "late_assessment": assessment.as_dict()})
        return result

    def snapshot(self, *, maximum_days: int = 7) -> ShipmentMonitorSnapshot:
        shipments = self.assess(maximum_days=maximum_days)
        statuses = Counter(str(row.get("status", "unknown")) for row in shipments)
        return ShipmentMonitorSnapshot(
            active=len(shipments),
            late=sum(bool(row["late_assessment"]["late"]) for row in shipments),
            exceptions=statuses.get("exception", 0),
            by_status=dict(statuses),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
