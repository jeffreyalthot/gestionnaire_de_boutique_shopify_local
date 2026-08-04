from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from threading import RLock


class VelocityGuard:
    def __init__(self, limit: int = 5, window_seconds: int = 3600) -> None:
        self.limit = limit
        self.window = timedelta(seconds=window_seconds)
        self._events: dict[str, deque[datetime]] = defaultdict(deque)
        self._lock = RLock()

    def register(self, key: str, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        with self._lock:
            events = self._events[key]
            while events and now - events[0] > self.window:
                events.popleft()
            if len(events) >= self.limit:
                return False
            events.append(now)
            return True
