from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


class OperationCheckpoint:
    def __init__(self, db: Any, operation: str) -> None:
        self.db = db
        self.operation = operation

    def save(self, key: str, state: dict[str, Any], status: str = "saved") -> None:
        self.db.execute(
            "INSERT INTO operation_checkpoints(operation,checkpoint_key,state_json,status,updated_at) VALUES(?,?,?,?,?) "
            "ON CONFLICT(operation,checkpoint_key) DO UPDATE SET state_json=excluded.state_json,status=excluded.status,updated_at=excluded.updated_at",
            (self.operation, key, json.dumps(state, ensure_ascii=False, default=str), status, datetime.now(timezone.utc).isoformat()),
        )

    def load(self, key: str, default: Any = None) -> Any:
        row = self.db.query_one("SELECT state_json FROM operation_checkpoints WHERE operation=? AND checkpoint_key=?", (self.operation, key))
        return json.loads(row["state_json"]) if row else default

    def clear(self, key: str) -> None:
        self.db.execute("DELETE FROM operation_checkpoints WHERE operation=? AND checkpoint_key=?", (self.operation, key))
