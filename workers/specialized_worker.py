from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from time import monotonic
from typing import Any, Callable

from workers.worker_budget import WorkerBudget


@dataclass(frozen=True)
class WorkerRunResult:
    worker: str
    task_type: str
    status: str
    result: Any = None
    duration_ms: float = 0.0
    attempts: int = 1
    error: str = ""
    completed_at: str = ""

    def as_dict(self) -> dict[str, object]: return asdict(self)


class SpecializedWorker:
    name = "specialized"
    queue = "default"
    accepted_task_types: tuple[str, ...] = ()

    def __init__(self, handler: Callable[[dict[str, Any]], Any], budget: WorkerBudget | None = None, *, timeout_seconds: float = 60, retries: int = 0) -> None:
        self.handler = handler; self.budget = budget or WorkerBudget(1); self.timeout_seconds = max(.1, float(timeout_seconds)); self.retries = max(0, int(retries)); self.last_result: WorkerRunResult | None = None

    async def run_once(self, task_type: str, payload: dict[str, Any]) -> WorkerRunResult:
        started = monotonic()
        if task_type not in self.accepted_task_types:
            self.budget.rejected += 1
            return WorkerRunResult(self.name, task_type, "rejected", duration_ms=round((monotonic() - started) * 1000, 3), error="unsupported_task_type", completed_at=datetime.now(timezone.utc).isoformat())
        error = ""
        for attempt in range(1, self.retries + 2):
            try:
                async with self.budget.slot():
                    async def invoke():
                        result = self.handler(dict(payload))
                        return await result if asyncio.iscoroutine(result) else result
                    value = await asyncio.wait_for(invoke(), timeout=self.timeout_seconds)
                self.last_result = WorkerRunResult(self.name, task_type, "completed", value, round((monotonic() - started) * 1000, 3), attempt, completed_at=datetime.now(timezone.utc).isoformat())
                return self.last_result
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"[:1000]
                if attempt <= self.retries: await asyncio.sleep(min(1.0, .05 * (2 ** attempt)))
        self.last_result = WorkerRunResult(self.name, task_type, "failed", duration_ms=round((monotonic() - started) * 1000, 3), attempts=self.retries + 1, error=error, completed_at=datetime.now(timezone.utc).isoformat())
        return self.last_result
