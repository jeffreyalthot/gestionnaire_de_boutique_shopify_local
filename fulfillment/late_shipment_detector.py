from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class LateShipmentAssessment:
    late: bool
    age_days: float
    overdue_days: float
    severity: str
    next_action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class LateShipmentDetector:
    def assess(self, updated_at: str | datetime, maximum_days: int, *, now: datetime | None = None) -> LateShipmentAssessment:
        if maximum_days < 0:
            raise ValueError("maximum_days invalide")
        dt = updated_at if isinstance(updated_at, datetime) else datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        current = now or datetime.now(timezone.utc)
        age = max(0.0, (current - dt.astimezone(timezone.utc)).total_seconds() / 86400)
        overdue = max(0.0, age - maximum_days)
        severity = "none" if overdue <= 0 else "low" if overdue < 2 else "medium" if overdue < 7 else "high"
        action = "none" if severity == "none" else "refresh_tracking" if severity == "low" else "contact_carrier" if severity == "medium" else "open_claim"
        return LateShipmentAssessment(overdue > 0, round(age, 2), round(overdue, 2), severity, action)


def is_late(updated_at: str, maximum_days: int) -> bool:
    return LateShipmentDetector().assess(updated_at, maximum_days).late
