from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class LeaseRecoveryResult:
    recovered: int
    checked_at: str
    healthy: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class LeaseManager:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.recovered_total = 0

    def recover(self) -> LeaseRecoveryResult:
        count = int(self.db.purge_expired_leases())
        self.recovered_total += count
        return LeaseRecoveryResult(count, datetime.now(timezone.utc).isoformat(), True)


def recover_expired_leases(db: Database) -> int:
    return LeaseManager(db).recover().recovered
