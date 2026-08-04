from __future__ import annotations
from dataclasses import dataclass, field
from threading import Lock
from time import time

@dataclass
class MetricsRegistry:
    counters: dict[str, float] = field(default_factory=dict)
    gauges: dict[str, float] = field(default_factory=dict)
    updated_at: float = field(default_factory=time)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def inc(self, name: str, value: float = 1) -> None:
        with self._lock:
            self.counters[name] = self.counters.get(name, 0) + value
            self.updated_at = time()

    def set(self, name: str, value: float) -> None:
        with self._lock:
            self.gauges[name] = value
            self.updated_at = time()

    def snapshot(self) -> dict[str, dict[str, float]]:
        with self._lock:
            return {"counters": dict(self.counters), "gauges": dict(self.gauges), "updated_at": self.updated_at}

metrics = MetricsRegistry()
