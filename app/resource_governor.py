from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Iterator

from automation.core.runtime_budget import ResourceGovernor as _ResourceGovernor
from automation.core.runtime_budget import RuntimeBudget


@dataclass(frozen=True, slots=True)
class ResourcePermit:
    allowed: bool
    reason: str
    heavy: bool
    pending_tasks: int
    acquired_at: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ResourceGovernor(_ResourceGovernor):
    """Façade applicative ajoutant des permis et des métriques d'opération."""

    def __init__(self, budget: RuntimeBudget) -> None:
        super().__init__(budget)
        self._operations_started = 0
        self._operations_rejected = 0
        self._operation_seconds = 0.0

    def request(self, *, heavy: bool = False, pending_tasks: int = 0) -> ResourcePermit:
        allowed, reason = self.allow(heavy=heavy, pending_tasks=pending_tasks)
        if allowed:
            self._operations_started += 1
        else:
            self._operations_rejected += 1
        return ResourcePermit(allowed, reason, heavy, max(0, int(pending_tasks)), monotonic())

    @contextmanager
    def operation(self, *, heavy: bool = False, pending_tasks: int = 0) -> Iterator[ResourcePermit]:
        permit = self.request(heavy=heavy, pending_tasks=pending_tasks)
        if not permit.allowed:
            raise RuntimeError(permit.reason)
        started = monotonic()
        try:
            yield permit
        finally:
            self._operation_seconds += monotonic() - started

    def operational_stats(self) -> dict[str, object]:
        sample = self.sample()
        sample.update({
            "operations_started": self._operations_started,
            "operations_rejected": self._operations_rejected,
            "operation_seconds": round(self._operation_seconds, 4),
        })
        return sample


__all__ = ["ResourceGovernor", "RuntimeBudget", "ResourcePermit"]
