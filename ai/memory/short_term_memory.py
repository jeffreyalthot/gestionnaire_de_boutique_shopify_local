from __future__ import annotations

from collections import Counter, deque
from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock
from typing import Callable


class ShortTermMemory:
    """Thread-safe bounded event memory for inference and operator diagnostics."""

    def __init__(self, maximum: int = 500) -> None:
        if maximum <= 0:
            raise ValueError("maximum must be positive")
        self.items: deque[dict[str, object]] = deque(maxlen=int(maximum))
        self._lock = RLock()
        self._added = 0
        self._evicted = 0

    def add(self, item: dict[str, object]) -> None:
        if not isinstance(item, dict):
            raise TypeError("item must be a dict")
        event = deepcopy(item)
        event.setdefault("recorded_at", datetime.now(timezone.utc).isoformat())
        with self._lock:
            if len(self.items) == self.items.maxlen:
                self._evicted += 1
            self.items.append(event)
            self._added += 1

    def recent(self, count: int = 20) -> list[dict[str, object]]:
        with self._lock:
            return deepcopy(list(self.items)[-max(0, int(count)):])

    def query(
        self,
        *,
        event_type: str | None = None,
        predicate: Callable[[dict[str, object]], bool] | None = None,
        limit: int = 100,
        **filters: object,
    ) -> list[dict[str, object]]:
        with self._lock:
            values = list(self.items)
        result: list[dict[str, object]] = []
        requested_type = event_type if event_type is not None else filters.pop("type", None)
        for item in reversed(values):
            if requested_type is not None and str(item.get("type", "")) != str(requested_type):
                continue
            if filters and any(item.get(key) != value for key, value in filters.items()):
                continue
            if predicate is not None and not predicate(item):
                continue
            result.append(deepcopy(item))
            if len(result) >= max(1, int(limit)):
                break
        result.reverse()
        return result

    def clear(self) -> int:
        with self._lock:
            count = len(self.items)
            self.items.clear()
            return count

    def stats(self) -> dict[str, object]:
        with self._lock:
            kinds = Counter(str(item.get("type", "unknown")) for item in self.items)
            return {
                "size": len(self.items),
                "capacity": self.items.maxlen,
                "added": self._added,
                "evicted": self._evicted,
                "types": dict(kinds),
            }
