from __future__ import annotations

import os
from collections import deque
from statistics import mean
from typing import Any

import psutil


class ResourceMonitor:
    def __init__(self, *, history_size: int = 60) -> None:
        self.process = psutil.Process(os.getpid())
        self.history: deque[dict[str, float]] = deque(maxlen=max(2, int(history_size)))

    def snapshot(self) -> dict[str, float]:
        memory = self.process.memory_info()
        value = {
            "rss_mb": round(memory.rss / 1048576, 2),
            "vms_mb": round(memory.vms / 1048576, 2),
            "cpu_percent": round(self.process.cpu_percent(None), 2),
            "system_memory_percent": round(psutil.virtual_memory().percent, 2),
            "threads": float(self.process.num_threads()),
            "open_files": float(len(self.process.open_files())),
        }
        self.history.append(value)
        return value

    def summary(self) -> dict[str, Any]:
        if not self.history:
            self.snapshot()
        keys = ("rss_mb", "cpu_percent", "system_memory_percent", "threads")
        return {
            "samples": len(self.history),
            "average": {key: round(mean(row[key] for row in self.history), 2) for key in keys},
            "maximum": {key: max(row[key] for row in self.history) for key in keys},
            "latest": dict(self.history[-1]),
        }
