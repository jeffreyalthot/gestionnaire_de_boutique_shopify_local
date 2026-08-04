from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from time import monotonic
from typing import Any, Awaitable, Callable, Iterable
from uuid import uuid4

StepCallable = Callable[[dict[str, Any]], dict[str, Any] | Awaitable[dict[str, Any]]]


@dataclass(frozen=True)
class WorkflowStep:
    name: str
    action: StepCallable
    mutating: bool = False
    approval_required: bool = False
    retry_limit: int = 0
    timeout_seconds: float = 60.0
    compensation: StepCallable | None = None


@dataclass(frozen=True)
class WorkflowStepResult:
    name: str
    status: str
    detail: dict[str, Any] = field(default_factory=dict)
    attempts: int = 1
    duration_seconds: float = 0.0


@dataclass(frozen=True)
class WorkflowResult:
    workflow_id: str
    name: str
    status: str
    dry_run: bool
    started_at: str
    finished_at: str
    steps: tuple[WorkflowStepResult, ...]
    context: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["steps"] = [asdict(step) for step in self.steps]
        return value


class WorkflowError(RuntimeError):
    pass


class BaseWorkflow:
    """Auditable workflow with retries, timeouts and reverse compensation."""

    name = "workflow"

    def __init__(self, container: Any | None = None) -> None:
        self.container = container

    def steps(self) -> Iterable[WorkflowStep]:
        return ()

    async def execute(self, payload: dict[str, Any] | None = None, *, dry_run: bool | None = None,
                      approved: bool = False) -> WorkflowResult:
        context = dict(payload or {})
        if dry_run is None:
            settings = getattr(self.container, "settings", None)
            dry_run = bool(getattr(settings, "app_dry_run", True))
        workflow_id = str(uuid4())
        context.setdefault("workflow_id", workflow_id)
        started = datetime.now(timezone.utc).isoformat()
        results: list[WorkflowStepResult] = []
        completed: list[WorkflowStep] = []
        status = "completed"
        for step in self.steps():
            if step.approval_required and not approved:
                results.append(WorkflowStepResult(step.name, "approval_required", attempts=0))
                status = "waiting_approval"
                break
            if step.mutating and dry_run:
                results.append(WorkflowStepResult(step.name, "simulated", {"mutation_suppressed": True}, 0, 0.0))
                continue
            started_step = monotonic()
            detail: dict[str, Any] = {}
            failure: Exception | None = None
            attempts = 0
            for attempt in range(max(0, int(step.retry_limit)) + 1):
                attempts = attempt + 1
                try:
                    value = step.action(context)
                    if asyncio.iscoroutine(value):
                        value = await asyncio.wait_for(value, timeout=max(.01, float(step.timeout_seconds)))
                    detail = dict(value or {})
                    context.update(detail)
                    failure = None
                    break
                except Exception as exc:
                    failure = exc
                    if attempt < step.retry_limit:
                        await asyncio.sleep(min(2.0, 0.05 * (2 ** attempt)))
            duration = monotonic() - started_step
            if failure is not None:
                results.append(WorkflowStepResult(step.name, "failed", {
                    "error_type": type(failure).__name__, "error": str(failure)[:2000],
                }, attempts, duration))
                status = "failed"
                await self._compensate(completed, context, results)
                break
            completed.append(step)
            results.append(WorkflowStepResult(step.name, "completed", detail, attempts, duration))
        finished = datetime.now(timezone.utc).isoformat()
        result = WorkflowResult(workflow_id, self.name, status, bool(dry_run), started, finished,
                                tuple(results), dict(context))
        db = getattr(self.container, "db", None)
        if db is not None:
            db.insert_audit(f"workflow.{self.name}", "workflow-runtime", result.as_dict())
            db.set_value(f"workflow:last:{self.name}", result.as_dict())
        return result

    async def _compensate(self, completed: list[WorkflowStep], context: dict[str, Any],
                          results: list[WorkflowStepResult]) -> None:
        for step in reversed(completed):
            if step.compensation is None:
                continue
            started = monotonic()
            try:
                value = step.compensation(context)
                if asyncio.iscoroutine(value):
                    value = await asyncio.wait_for(value, timeout=max(.01, float(step.timeout_seconds)))
                results.append(WorkflowStepResult(f"compensate:{step.name}", "completed", dict(value or {}), 1, monotonic() - started))
            except Exception as exc:
                results.append(WorkflowStepResult(f"compensate:{step.name}", "failed", {
                    "error_type": type(exc).__name__, "error": str(exc)[:2000],
                }, 1, monotonic() - started))


@dataclass(frozen=True, slots=True)
class ServiceWorkflowRun:
    name: str
    status: str
    attempts: int
    duration_ms: float
    started_at: str
    finished_at: str
    result: Any = None
    error: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ServiceWorkflow:
    """Compatibility adapter for a service method with retries and metrics.

    It intentionally returns the raw service result from ``execute`` so older
    callers keep working, while ``last_run`` exposes the auditable envelope.
    """

    name = "service_workflow"
    method_candidates: tuple[str, ...] = ("execute", "run")

    def __init__(self, service: Any, *, timeout_seconds: float = 120.0, retries: int = 1) -> None:
        self.service = service
        self.timeout_seconds = max(0.1, float(timeout_seconds))
        self.retries = max(0, min(int(retries), 5))
        self.runs = self.completed = self.failed = 0
        self.last_run: ServiceWorkflowRun | None = None

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        started_at = datetime.now(timezone.utc).isoformat()
        started = monotonic()
        self.runs += 1
        failure: Exception | None = None
        for attempt in range(1, self.retries + 2):
            try:
                method = next((getattr(self.service, name, None) for name in self.method_candidates if callable(getattr(self.service, name, None))), None)
                if method is None:
                    raise AttributeError("Service incompatible avec ce workflow: " + ", ".join(self.method_candidates))
                value = method(*args, **kwargs)
                if asyncio.iscoroutine(value):
                    value = await asyncio.wait_for(value, timeout=self.timeout_seconds)
                self.completed += 1
                self.last_run = ServiceWorkflowRun(
                    self.name, "completed", attempt, round((monotonic() - started) * 1000, 3),
                    started_at, datetime.now(timezone.utc).isoformat(), value,
                )
                return value
            except Exception as exc:
                failure = exc
                if attempt <= self.retries:
                    await asyncio.sleep(min(2.0, 0.05 * (2 ** (attempt - 1))))
        self.failed += 1
        assert failure is not None
        self.last_run = ServiceWorkflowRun(
            self.name, "failed", self.retries + 1, round((monotonic() - started) * 1000, 3),
            started_at, datetime.now(timezone.utc).isoformat(), error=f"{type(failure).__name__}: {failure}"[:2000],
        )
        raise failure

    def stats(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "runs": self.runs,
            "completed": self.completed,
            "failed": self.failed,
            "success_rate": round(self.completed / self.runs, 6) if self.runs else 1.0,
            "last": self.last_run.as_dict() if self.last_run else None,
        }
