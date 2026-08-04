from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from time import monotonic
from typing import AsyncIterator


@dataclass(frozen=True)
class WorkerBudgetSnapshot:
    active: int
    completed: int
    failed: int
    rejected: int
    concurrency: int
    waiting: int = 0
    acquired_total: int = 0
    average_wait_ms: float = 0.0
    peak_active: int = 0


class WorkerBudget:
    """Budget de concurrence commun, borné à deux tâches pour le profil 2 Go."""

    def __init__(self, concurrency: int = 1) -> None:
        if not 1 <= concurrency <= 2: raise ValueError("La concurrence worker doit rester entre 1 et 2.")
        self.concurrency = concurrency; self._semaphore = asyncio.Semaphore(concurrency)
        self.active = self.completed = self.failed = self.rejected = 0
        self.waiting = self.acquired_total = self.peak_active = 0; self._wait_total = 0.0

    @asynccontextmanager
    async def slot(self) -> AsyncIterator[None]:
        started = monotonic(); self.waiting += 1
        await self._semaphore.acquire(); self.waiting = max(0, self.waiting - 1)
        self._wait_total += monotonic() - started; self.acquired_total += 1; self.active += 1; self.peak_active = max(self.peak_active, self.active)
        try:
            yield
        except Exception:
            self.failed += 1; raise
        else:
            self.completed += 1
        finally:
            self.active -= 1; self._semaphore.release()

    def snapshot(self) -> dict[str, int | float]:
        average = self._wait_total / self.acquired_total * 1000 if self.acquired_total else 0.0
        return asdict(WorkerBudgetSnapshot(self.active, self.completed, self.failed, self.rejected, self.concurrency, self.waiting, self.acquired_total, round(average, 3), self.peak_active))
