from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from time import monotonic
from typing import Any, ClassVar, Mapping

from workers.worker_budget import WorkerBudget


@dataclass(frozen=True, slots=True)
class WorkerExecution:
    worker: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: float
    attempts: int
    payload_fingerprint: str
    result: Any = None
    error: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class DelegatingWorker:
    """Low-resource service worker with timeout, retry and instrumentation."""

    name: ClassVar[str] = "worker"
    queue: ClassVar[str] = "default"
    method_candidates: ClassVar[tuple[str, ...]] = ("execute",)

    def __init__(
        self,
        service: Any,
        *,
        timeout_seconds: float = 60.0,
        retries: int = 1,
        budget: WorkerBudget | None = None,
    ) -> None:
        self.service = service
        self.timeout_seconds = max(0.1, float(timeout_seconds))
        self.retries = max(0, min(int(retries), 5))
        self.budget = budget or WorkerBudget(1)
        self.runs = self.completed = self.failed = 0
        self.last_execution: WorkerExecution | None = None

    async def run(self, payload: dict[str, object]) -> object:
        execution = await self.execute(payload)
        if execution.status != "completed":
            raise RuntimeError(execution.error or f"Échec worker {self.name}")
        return execution.result

    async def execute(self, payload: Mapping[str, object] | None = None) -> WorkerExecution:
        normalized = dict(payload or {})
        fingerprint = hashlib.sha256(
            json.dumps(normalized, ensure_ascii=False, default=str, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:24]
        started_at = datetime.now(timezone.utc).isoformat()
        started = monotonic()
        self.runs += 1
        error = ""
        for attempt in range(1, self.retries + 2):
            try:
                async with self.budget.slot():
                    value = await asyncio.wait_for(self._invoke(normalized), timeout=self.timeout_seconds)
                self.completed += 1
                execution = WorkerExecution(
                    self.name,
                    "completed",
                    started_at,
                    datetime.now(timezone.utc).isoformat(),
                    round((monotonic() - started) * 1000, 3),
                    attempt,
                    fingerprint,
                    value,
                )
                self.last_execution = execution
                return execution
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"[:2000]
                if attempt <= self.retries:
                    await asyncio.sleep(min(2.0, 0.05 * (2 ** (attempt - 1))))
        self.failed += 1
        execution = WorkerExecution(
            self.name,
            "failed",
            started_at,
            datetime.now(timezone.utc).isoformat(),
            round((monotonic() - started) * 1000, 3),
            self.retries + 1,
            fingerprint,
            error=error,
        )
        self.last_execution = execution
        return execution

    async def _invoke(self, payload: dict[str, object]) -> object:
        method = next((getattr(self.service, name, None) for name in self.method_candidates if callable(getattr(self.service, name, None))), None)
        if method is None:
            raise AttributeError(
                f"Le service de {self.name} ne fournit aucune méthode parmi: {', '.join(self.method_candidates)}"
            )
        result = method(payload)
        return await result if asyncio.iscoroutine(result) else result

    def stats(self) -> dict[str, object]:
        return {
            "name": self.name,
            "queue": self.queue,
            "runs": self.runs,
            "completed": self.completed,
            "failed": self.failed,
            "success_rate": round(self.completed / self.runs, 6) if self.runs else 1.0,
            "budget": self.budget.snapshot(),
            "last": self.last_execution.as_dict() if self.last_execution else None,
        }
