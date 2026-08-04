from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock


@dataclass(frozen=True, slots=True)
class TranslationEntry:
    source: str
    source_locale: str
    target_locale: str
    translated: str
    quality: float
    updated_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class TranslationMemory:
    def __init__(self, path: str | Path | None = None, *, maximum_entries: int = 5000) -> None:
        self._values: dict[tuple[str, str, str], TranslationEntry] = {}
        self.maximum_entries = max(1, int(maximum_entries))
        self.path = Path(path) if path else None
        self._lock = RLock()
        if self.path:
            self._initialize()

    def put(self, source: str, source_locale: str, target_locale: str, translated: str, *, quality: float = 1.0) -> None:
        key = self._key(source, source_locale, target_locale)
        entry = TranslationEntry(source.strip(), source_locale, target_locale, translated.strip(), max(0.0, min(1.0, quality)), datetime.now(timezone.utc).isoformat())
        with self._lock:
            self._values[key] = entry
            while len(self._values) > self.maximum_entries:
                self._values.pop(next(iter(self._values)))
            if self.path:
                with sqlite3.connect(self.path) as db:
                    db.execute("INSERT OR REPLACE INTO translations VALUES (?,?,?,?,?,?)", (entry.source_locale, entry.target_locale, entry.source, entry.translated, entry.quality, entry.updated_at))

    def get(self, source: str, source_locale: str, target_locale: str) -> str | None:
        key = self._key(source, source_locale, target_locale)
        with self._lock:
            entry = self._values.get(key)
            if entry:
                return entry.translated
        if self.path:
            with sqlite3.connect(self.path) as db:
                row = db.execute("SELECT translated,quality,updated_at FROM translations WHERE source_locale=? AND target_locale=? AND source=?", key).fetchone()
            if row:
                self._values[key] = TranslationEntry(key[2], key[0], key[1], row[0], row[1], row[2])
                return row[0]
        return None

    def stats(self) -> dict[str, object]:
        return {"entries": len(self._values), "persistent": bool(self.path), "maximum_entries": self.maximum_entries}

    @staticmethod
    def _key(source: str, source_locale: str, target_locale: str) -> tuple[str, str, str]:
        return source_locale.strip(), target_locale.strip(), source.strip()

    def _initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS translations(source_locale TEXT,target_locale TEXT,source TEXT,translated TEXT,quality REAL,updated_at TEXT,PRIMARY KEY(source_locale,target_locale,source))")
