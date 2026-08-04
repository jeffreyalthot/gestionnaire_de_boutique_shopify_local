from collections import Counter
from threading import Lock

class ThreadSafeCounters:
    def __init__(self) -> None:
        self._values: Counter[str] = Counter()
        self._lock = Lock()
    def increment(self, name: str, value: int = 1) -> None:
        with self._lock: self._values[name] += value
    def snapshot(self) -> dict[str, int]:
        with self._lock: return dict(self._values)
