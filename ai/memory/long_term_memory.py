from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    key: str
    value: Any
    updated_at: str
    expires_at: str = ""
    tags: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class LongTermMemory:
    """SQLite-backed memory namespace with optional expiration and tags."""

    namespace = "ai-memory"

    def __init__(self, db: Database, *, namespace: str | None = None) -> None:
        self.db = db
        self.namespace = (namespace or self.namespace).strip(":")

    def _storage_key(self, key: str) -> str:
        clean = str(key).strip()
        if not clean:
            raise ValueError("memory key is required")
        return f"{self.namespace}:{clean}"

    def remember(
        self,
        key: str,
        value: object,
        *,
        ttl_seconds: float | None = None,
        tags: Iterable[str] = (),
    ) -> None:
        now = datetime.now(timezone.utc)
        expires_at = ""
        if ttl_seconds is not None:
            expires_at = (now + timedelta(seconds=max(0.0, float(ttl_seconds)))).isoformat()
        envelope = {
            "_memory_record": 1,
            "value": value,
            "updated_at": now.isoformat(),
            "expires_at": expires_at,
            "tags": sorted({str(tag).strip() for tag in tags if str(tag).strip()}),
        }
        self.db.set_value(self._storage_key(key), envelope)

    def recall(self, key: str, default: Any = None) -> Any:
        raw = self.db.get_value(self._storage_key(key), default)
        if not isinstance(raw, dict) or raw.get("_memory_record") != 1:
            return raw
        if self._expired(str(raw.get("expires_at", ""))):
            self.forget(key)
            return default
        return raw.get("value", default)

    def record(self, key: str) -> MemoryRecord | None:
        raw = self.db.get_value(self._storage_key(key))
        if raw is None:
            return None
        if not isinstance(raw, dict) or raw.get("_memory_record") != 1:
            return MemoryRecord(str(key), raw, "")
        if self._expired(str(raw.get("expires_at", ""))):
            self.forget(key)
            return None
        return MemoryRecord(
            key=str(key),
            value=raw.get("value"),
            updated_at=str(raw.get("updated_at", "")),
            expires_at=str(raw.get("expires_at", "")),
            tags=tuple(str(item) for item in raw.get("tags", ())),
        )

    def forget(self, key: str) -> bool:
        return bool(self.db.execute("DELETE FROM key_values WHERE key=?", (self._storage_key(key),)))

    def contains(self, key: str) -> bool:
        return self.record(key) is not None

    def keys(self, prefix: str = "", *, limit: int = 1000) -> tuple[str, ...]:
        storage_prefix = self._storage_key(prefix) if prefix else f"{self.namespace}:"
        rows = self.db.query(
            "SELECT key FROM key_values WHERE key LIKE ? ORDER BY key LIMIT ?",
            (storage_prefix + "%", max(1, min(int(limit), 10_000))),
        )
        base = f"{self.namespace}:"
        return tuple(str(row["key"])[len(base):] for row in rows)

    def scan(self, prefix: str = "", *, limit: int = 1000) -> tuple[MemoryRecord, ...]:
        records: list[MemoryRecord] = []
        for key in self.keys(prefix, limit=limit):
            record = self.record(key)
            if record is not None:
                records.append(record)
        return tuple(records)

    def prune_expired(self, *, limit: int = 1000) -> int:
        removed = 0
        for record in self.scan(limit=limit):
            if self._expired(record.expires_at):
                removed += int(self.forget(record.key))
        return removed

    @staticmethod
    def _expired(value: str) -> bool:
        if not value:
            return False
        try:
            return datetime.fromisoformat(value) <= datetime.now(timezone.utc)
        except ValueError:
            return True
