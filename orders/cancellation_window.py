from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True, slots=True)
class CancellationWindowDecision:
    allowed: bool
    reason: str
    closes_at: str
    remaining_seconds: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CancellationWindow:
    def __init__(self, window_minutes: int = 30) -> None:
        self.window_minutes = max(0, int(window_minutes))

    def evaluate(self, created_at: datetime, *, supplier_submitted: bool = False,
                 now: datetime | None = None) -> CancellationWindowDecision:
        current = now or datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        closes = created_at + timedelta(minutes=self.window_minutes)
        remaining = max(0, int((closes - current).total_seconds()))
        if supplier_submitted:
            return CancellationWindowDecision(False, "supplier_submitted", closes.isoformat(), remaining)
        allowed = current <= closes
        return CancellationWindowDecision(allowed, "within_window" if allowed else "window_expired", closes.isoformat(), remaining)

    def allowed(self, created_at: datetime, now: datetime | None = None) -> bool:
        return self.evaluate(created_at, now=now).allowed

    def can_cancel(self, created_at: datetime, now: datetime | None = None) -> bool:
        return self.allowed(created_at, now)


def can_cancel(created_at: datetime, *, supplier_submitted: bool, window_minutes: int = 30,
               now: datetime | None = None) -> bool:
    return CancellationWindow(window_minutes).evaluate(created_at, supplier_submitted=supplier_submitted, now=now).allowed
