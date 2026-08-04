from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from time import monotonic


@dataclass(frozen=True, slots=True)
class PoolStats:
    maximum: int
    active: int
    waiting: int
    acquired_total: int
    timeout_total: int
    average_wait_seconds: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ConnectionLimiter:
    def __init__(self, maximum: int) -> None:
        self.maximum = max(1, int(maximum))
        self.semaphore = asyncio.Semaphore(self.maximum)
        self._active = self._waiting = self._acquired = self._timeouts = 0
        self._wait_total = 0.0
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def slot(self, timeout_seconds: float | None = None):
        started = monotonic()
        async with self._lock:
            self._waiting += 1
        try:
            if timeout_seconds is None:
                await self.semaphore.acquire()
            else:
                await asyncio.wait_for(self.semaphore.acquire(), timeout=max(0.001, timeout_seconds))
        except TimeoutError:
            async with self._lock:
                self._timeouts += 1
            raise
        finally:
            async with self._lock:
                self._waiting = max(0, self._waiting - 1)
        waited = monotonic() - started
        async with self._lock:
            self._active += 1; self._acquired += 1; self._wait_total += waited
        try:
            yield
        finally:
            self.semaphore.release()
            async with self._lock:
                self._active = max(0, self._active - 1)

    def stats(self) -> PoolStats:
        average = self._wait_total / self._acquired if self._acquired else 0.0
        return PoolStats(self.maximum, self._active, self._waiting, self._acquired, self._timeouts, round(average, 6))
