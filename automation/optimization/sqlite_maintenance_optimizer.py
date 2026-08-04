from __future__ import annotations

from typing import Any


class SqliteMaintenanceOptimizer:
    def inspect(self, db: Any) -> dict[str, int | bool]:
        with db.connect() as conn:
            pages = int(conn.execute("PRAGMA page_count").fetchone()[0])
            free = int(conn.execute("PRAGMA freelist_count").fetchone()[0])
            wal = int(conn.execute("PRAGMA wal_autocheckpoint").fetchone()[0])
        ratio = free / max(1, pages)
        return {"page_count": pages, "free_pages": free, "free_ratio": round(ratio, 4), "wal_autocheckpoint": wal, "vacuum_recommended": ratio > 0.25}

    def maintain(self, db: Any, *, allow_vacuum: bool = False) -> dict[str, object]:
        before = self.inspect(db)
        with db.connect() as conn:
            conn.execute("PRAGMA optimize")
            conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
            if allow_vacuum and before["vacuum_recommended"]:
                conn.execute("VACUUM")
        return {"before": before, "after": self.inspect(db)}
