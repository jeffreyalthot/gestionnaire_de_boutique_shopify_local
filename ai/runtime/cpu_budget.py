from __future__ import annotations

import os
from collections import deque
from dataclasses import asdict, dataclass
from statistics import fmean

import psutil


@dataclass(frozen=True, slots=True)
class CPUSnapshot:
    current_percent: float
    average_percent: float
    maximum_percent: float
    overloaded: bool
    samples: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CPUBudget:
    def __init__(self, maximum_percent: float, history: int = 10) -> None:
        self.maximum = max(1.0, float(maximum_percent))
        self.process = psutil.Process(os.getpid())
        self.values: deque[float] = deque(maxlen=max(1, int(history)))

    def current(self) -> float:
        value = max(0.0, self.process.cpu_percent(interval=None))
        self.values.append(value)
        return value

    def snapshot(self) -> CPUSnapshot:
        current = self.current()
        average = fmean(self.values) if self.values else current
        return CPUSnapshot(round(current, 2), round(average, 2), self.maximum, max(current, average) > self.maximum, len(self.values))

    def overloaded(self) -> bool:
        return self.snapshot().overloaded
