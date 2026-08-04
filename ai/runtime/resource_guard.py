from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from threading import RLock
from time import monotonic
from typing import Iterator

from ai.runtime.cpu_budget import CPUBudget
from ai.runtime.memory_budget import MemoryBudget


@dataclass(frozen=True, slots=True)
class GuardStats:
    entered: int
    completed: int
    rejected: int
    failed: int
    active: int
    total_seconds: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ResourceGuard:
    def __init__(self, memory: MemoryBudget, cpu: CPUBudget) -> None:
        self.memory = memory
        self.cpu = cpu
        self._lock = RLock()
        self.entered = self.completed = self.rejected = self.failed = self.active = 0
        self.total_seconds = 0.0

    @contextmanager
    def inference(self, reserve_mb: float = 10) -> Iterator[None]:
        started = monotonic()
        with self._lock:
            self.entered += 1
        try:
            self.memory.require(reserve_mb)
            if self.cpu.overloaded():
                with self._lock: self.rejected += 1
                raise RuntimeError("CPU au-dessus du budget IA.")
            with self._lock: self.active += 1
            yield
        except Exception:
            with self._lock: self.failed += 1
            raise
        else:
            with self._lock: self.completed += 1
        finally:
            with self._lock:
                if self.active > 0: self.active -= 1
                self.total_seconds += monotonic() - started

    def stats(self) -> GuardStats:
        with self._lock:
            return GuardStats(self.entered, self.completed, self.rejected, self.failed, self.active, round(self.total_seconds, 6))
