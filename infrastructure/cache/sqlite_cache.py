from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class SQLiteCacheRecord:
    key: str
    value: object
    expires_at: str | None
    created_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SQLiteCache:
    def __init__(self, db: Database, prefix: str = "cache") -> None:
        self.db = db
        self.prefix = str(prefix).strip() or "cache"
        self._hits = 0
        self._misses = 0

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    def set(self, key: str, value: object, ttl_seconds: int | None = None) -> None:
        now = datetime.now(timezone.utc)
        expires = (now + timedelta(seconds=max(1, int(ttl_seconds)))).isoformat() if ttl_seconds is not None else None
        self.db.set_value(self._key(key), SQLiteCacheRecord(str(key), value, expires, now.isoformat()).as_dict())

    def get(self, key: str, default=None):
        raw = self.db.get_value(self._key(key), None)
        if not isinstance(raw, dict) or "value" not in raw:
            self._misses += 1
            return default
        expires = raw.get("expires_at")
        if expires and datetime.fromisoformat(str(expires).replace("Z", "+00:00")) <= datetime.now(timezone.utc):
            self.delete(key)
            self._misses += 1
            return default
        self._hits += 1
        return raw["value"]

    def delete(self, key: str) -> bool:
        return bool(self.db.execute("DELETE FROM key_values WHERE key=?", (self._key(key),)))

    def get_or_set(self, key: str, factory, ttl_seconds: int | None = None):
        sentinel = object()
        value = self.get(key, sentinel)
        if value is not sentinel:
            return value
        value = factory()
        self.set(key, value, ttl_seconds)
        return value

    def stats(self) -> dict[str, int]:
        return {"hits": self._hits, "misses": self._misses}
