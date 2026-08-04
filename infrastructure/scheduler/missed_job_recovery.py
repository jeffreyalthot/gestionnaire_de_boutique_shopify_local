from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class MissedJob:
    name: str
    last_run: str
    expected_interval_seconds: int
    overdue_seconds: float
    action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def last_run(db: Database, name: str) -> str:
    return str(db.get_value(f"scheduler:last:{name}", ""))


def record_run(db: Database, name: str, timestamp: str) -> None:
    db.set_value(f"scheduler:last:{name}", timestamp)


class MissedJobRecovery:
    def __init__(self, db: Database) -> None:
        self.db = db

    def inspect(
        self,
        schedules: Iterable[tuple[str, int]],
        *,
        now: datetime | None = None,
        grace_seconds: int = 60,
    ) -> tuple[MissedJob, ...]:
        current = now or datetime.now(timezone.utc)
        result: list[MissedJob] = []
        for name, interval in schedules:
            interval = max(1, int(interval))
            stored = last_run(self.db, name)
            if not stored:
                result.append(MissedJob(name, "", interval, float(interval), "run_now"))
                continue
            timestamp = datetime.fromisoformat(stored.replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            overdue = max(0.0, (current - timestamp).total_seconds() - interval)
            if overdue > max(0, grace_seconds):
                action = "run_now" if overdue < interval * 3 else "run_and_reconcile"
                result.append(MissedJob(name, stored, interval, round(overdue, 2), action))
        return tuple(sorted(result, key=lambda job: (-job.overdue_seconds, job.name)))

    def mark_recovered(self, name: str, *, at: datetime | None = None) -> None:
        record_run(self.db, name, (at or datetime.now(timezone.utc)).isoformat())
