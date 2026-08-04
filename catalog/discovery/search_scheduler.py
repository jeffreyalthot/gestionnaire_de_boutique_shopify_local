from __future__ import annotations

from datetime import datetime, timedelta, timezone


class SearchScheduler:
    def __init__(self, minimum_interval_seconds: int = 900) -> None:
        self.minimum_interval = timedelta(seconds=max(60, minimum_interval_seconds))
        self._last_run: dict[str, datetime] = {}

    def due(self, key: str, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        previous = self._last_run.get(key)
        return previous is None or now - previous >= self.minimum_interval

    def mark(self, key: str, now: datetime | None = None) -> None:
        self._last_run[key] = now or datetime.now(timezone.utc)
