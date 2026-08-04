from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import monotonic
from typing import Awaitable, Iterable


@dataclass(frozen=True, slots=True)
class ShutdownResult:
    requested: int
    completed: int
    cancelled: int
    failed: int
    timed_out: int
    duration_ms: float


async def cancel_tasks(tasks: list[asyncio.Task], *, timeout: float = 10.0) -> ShutdownResult:
    """Annule des tâches sans bloquer indéfiniment l'arrêt de Windows."""
    started = monotonic()
    active = [task for task in tasks if task is not None and not task.done()]
    for task in active:
        task.cancel()
    timed_out = 0
    if active:
        try:
            results = await asyncio.wait_for(asyncio.gather(*active, return_exceptions=True), timeout=max(0.05, timeout))
        except asyncio.TimeoutError:
            timed_out = sum(not task.done() for task in active)
            results = []
    else:
        results = []
    failed = sum(isinstance(item, BaseException) and not isinstance(item, asyncio.CancelledError) for item in results)
    cancelled = sum(task.cancelled() for task in active)
    completed = sum(task.done() and not task.cancelled() for task in active)
    return ShutdownResult(len(tasks), completed, cancelled, failed, timed_out, round((monotonic() - started) * 1000.0, 3))


async def run_cleanup(cleanups: Iterable[Awaitable[object]], *, timeout: float = 10.0) -> tuple[object, ...]:
    coroutines = tuple(cleanups)
    if not coroutines:
        return ()
    results = await asyncio.wait_for(asyncio.gather(*coroutines, return_exceptions=True), timeout=max(0.05, timeout))
    return tuple(results)
