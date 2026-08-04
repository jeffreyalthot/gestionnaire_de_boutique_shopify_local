from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from infrastructure.database.engine import Database, utcnow


class Heartbeat:
    def __init__(self, db: Database, name: str, *, stale_after_seconds: int = 120) -> None:
        self.db = db
        self.name = str(name).strip()
        if not self.name:
            raise ValueError("Nom de heartbeat requis.")
        self.stale_after_seconds = max(1, int(stale_after_seconds))
        self.beats = 0

    def beat(self, detail: dict[str, Any] | None = None) -> str:
        timestamp = utcnow()
        self.db.set_value(f"heartbeat:{self.name}", {"at": timestamp, "detail": dict(detail or {}), "count": self.beats + 1})
        self.beats += 1
        return timestamp

    def snapshot(self) -> dict[str, Any]:
        value = self.db.get_value(f"heartbeat:{self.name}", default={}) or {}
        raw = value.get("at") if isinstance(value, dict) else value
        age = None
        if raw:
            try:
                parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
                age = max(0.0, (datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).total_seconds())
            except ValueError:
                age = None
        return {"name": self.name, "at": raw, "age_seconds": age, "stale": age is None or age > self.stale_after_seconds, "beats": self.beats}
