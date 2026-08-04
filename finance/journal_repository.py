from __future__ import annotations

from typing import Any


class JournalRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def transaction(self, transaction_id: str) -> list[dict[str, Any]]:
        return self.db.query("SELECT * FROM ledger WHERE transaction_id=? ORDER BY rowid", (transaction_id,))

    def between(self, start: str, end: str, limit: int = 5000) -> list[dict[str, Any]]:
        return self.db.query("SELECT * FROM ledger WHERE created_at>=? AND created_at<? ORDER BY created_at LIMIT ?",
                             (start, end, max(1, min(limit, 10000))))
