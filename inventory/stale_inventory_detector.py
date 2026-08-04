from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class StaleInventoryAssessment:
    stale: bool
    age_seconds: float
    maximum_age_seconds: int
    severity: str
    action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class StaleInventoryDetector:
    def assess(
        self,
        updated_at: str | datetime,
        max_age_seconds: int,
        *,
        now: datetime | None = None,
    ) -> StaleInventoryAssessment:
        timestamp = (
            updated_at
            if isinstance(updated_at, datetime)
            else datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
        )
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)

        age = max(0.0, (current - timestamp.astimezone(timezone.utc)).total_seconds())
        maximum = max(1, int(max_age_seconds))
        ratio = age / maximum
        severity = (
            "none"
            if ratio <= 1
            else "low"
            if ratio < 2
            else "medium"
            if ratio < 5
            else "high"
        )
        action = (
            "none"
            if severity == "none"
            else "schedule_sync"
            if severity in {"low", "medium"}
            else "pause_sales"
        )
        return StaleInventoryAssessment(
            stale=ratio > 1,
            age_seconds=round(age, 2),
            maximum_age_seconds=maximum,
            severity=severity,
            action=action,
        )


def is_stale(updated_at: str, max_age_seconds: int) -> bool:
    return StaleInventoryDetector().assess(updated_at, max_age_seconds).stale
