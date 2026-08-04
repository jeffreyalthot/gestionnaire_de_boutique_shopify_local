from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class InferenceStats:
    submitted: int
    completed: int
    failed: int
    active: int
    total_seconds: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class InferenceScheduler:
    def __init__(self, workers: int = 1) -> None:
        self.workers = max(1, int(workers))
        self.semaphore = asyncio.Semaphore(self.workers)
        self.submitted = self.completed = self.failed = self.active = 0
        self.total_seconds = 0.0
        self._lock = asyncio.Lock()

    async def run(self, callable_: Callable[..., Any], *args: Any, timeout: float | None = None, **kwargs: Any) -> Any:
        async with self._lock:
            self.submitted += 1
        async with self.semaphore:
            async with self._lock:
                self.active += 1
            started = monotonic()
            try:
                task = asyncio.to_thread(callable_, *args, **kwargs)
                result = await asyncio.wait_for(task, timeout=timeout) if timeout is not None else await task
            except Exception:
                async with self._lock:
                    self.failed += 1
                raise
            else:
                async with self._lock:
                    self.completed += 1
                return result
            finally:
                elapsed = monotonic() - started
                async with self._lock:
                    self.active -= 1
                    self.total_seconds += elapsed

    def stats(self) -> InferenceStats:
        return InferenceStats(self.submitted, self.completed, self.failed, self.active, round(self.total_seconds, 6))
