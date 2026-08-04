from __future__ import annotations

from dataclasses import asdict, dataclass
from time import monotonic

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class DatabaseHealth:
    ok: bool
    latency_ms: float
    integrity: str
    journal_mode: str
    page_count: int
    freelist_count: int
    database_bytes: int
    counts: dict[str, int]
    error: str = ""

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DatabaseHealthChecker:
    def __init__(self, db: Database) -> None:
        self.db = db

    def inspect(self, *, quick_integrity: bool = True) -> DatabaseHealth:
        started = monotonic()
        try:
            integrity_query = "PRAGMA quick_check" if quick_integrity else "PRAGMA integrity_check"
            integrity = str(self.db.scalar(integrity_query, default="unknown"))
            page_count = int(self.db.scalar("PRAGMA page_count", default=0) or 0)
            page_size = int(self.db.scalar("PRAGMA page_size", default=0) or 0)
            freelist = int(self.db.scalar("PRAGMA freelist_count", default=0) or 0)
            journal_mode = str(self.db.scalar("PRAGMA journal_mode", default="unknown"))
            return DatabaseHealth(
                ok=integrity.lower() == "ok",
                latency_ms=round((monotonic() - started) * 1000, 3),
                integrity=integrity,
                journal_mode=journal_mode,
                page_count=page_count,
                freelist_count=freelist,
                database_bytes=page_count * page_size,
                counts=self.db.counts(),
            )
        except Exception as exc:
            return DatabaseHealth(False, round((monotonic() - started) * 1000, 3), "error", "unknown", 0, 0, 0, {}, str(exc)[:500])


def check_database(db: Database) -> dict[str, object]:
    basic = db.health()
    detailed = DatabaseHealthChecker(db).inspect().as_dict()
    return {**basic, "detailed": detailed}
