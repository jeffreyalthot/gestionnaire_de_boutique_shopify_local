from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from time import monotonic


class RequestBudget:
    def __init__(self, concurrency: int = 2, minimum_interval_seconds: float = 0.0) -> None:
        self._semaphore = asyncio.Semaphore(max(1, concurrency))
        self.minimum_interval = max(0.0, minimum_interval_seconds)
        self._last = 0.0
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def slot(self):
        async with self._semaphore:
            async with self._lock:
                delay = self.minimum_interval - (monotonic() - self._last)
                if delay > 0: await asyncio.sleep(delay)
                self._last = monotonic()
            yield
