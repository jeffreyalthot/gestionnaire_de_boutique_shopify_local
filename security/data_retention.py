from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True, slots=True)
class RetentionDecision:
    category: str
    cutoff: str
    retain_days: int
    delete_eligible: bool
    legal_hold: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DataRetentionPolicy:
    DEFAULTS = {"audit": 2555, "financial": 2555, "order": 2555, "customer_message": 730, "temporary": 7, "api_trace": 30}

    def __init__(self, rules: dict[str, int] | None = None) -> None:
        self.rules = {**self.DEFAULTS, **(rules or {})}

    def cutoff(self, category: str, *, now: datetime | None = None) -> datetime:
        days = max(0, int(self.rules.get(category, 365)))
        return (now or datetime.now(timezone.utc)) - timedelta(days=days)

    def evaluate(self, category: str, created_at: datetime, *, legal_hold: bool = False, now: datetime | None = None) -> RetentionDecision:
        current = now or datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        cutoff = self.cutoff(category, now=current)
        return RetentionDecision(category, cutoff.isoformat(), self.rules.get(category, 365), created_at < cutoff and not legal_hold, legal_hold)


def retention_cutoff(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=max(0, int(days)))).isoformat()
