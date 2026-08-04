from __future__ import annotations

from collections import deque
from datetime import datetime
from threading import RLock


class LogRingBuffer:
    def __init__(self, capacity: int = 8) -> None:
        if capacity < 1:
            raise ValueError("capacity doit être positif")
        self._items: deque[str] = deque(maxlen=capacity)
        self._lock = RLock()

    def append(self, message: str, level: str = "INFO") -> None:
        text = f"{datetime.now().strftime('%H:%M:%S')} [{level[:7]}] {message}"[:500]
        with self._lock:
            self._items.append(text)

    def lines(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._items)
