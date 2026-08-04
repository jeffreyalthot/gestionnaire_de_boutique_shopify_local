from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

from infrastructure.database.engine import utcnow


class SnapshotStore:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, snapshot: dict[str, Any]) -> str:
        identifier = str(uuid4())
        self.db.execute("INSERT INTO runtime_snapshots(id,snapshot_json,created_at) VALUES(?,?,?)", (identifier, json.dumps(snapshot, ensure_ascii=False, default=str), utcnow()))
        return identifier

    def latest(self) -> dict[str, Any] | None:
        row = self.db.query_one("SELECT snapshot_json FROM runtime_snapshots ORDER BY created_at DESC LIMIT 1")
        return json.loads(row["snapshot_json"]) if row else None
