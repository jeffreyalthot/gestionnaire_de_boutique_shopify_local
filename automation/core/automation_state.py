from __future__ import annotations

from dataclasses import asdict, dataclass, field
from threading import RLock
from typing import Any


@dataclass(slots=True)
class AutomationCounters:
    cycles: int = 0
    planned: int = 0
    accepted: int = 0
    rejected: int = 0
    completed: int = 0
    failed: int = 0
    retried: int = 0
    compensated: int = 0
    deferred: int = 0


class AutomationState:
    def __init__(self) -> None:
        self._lock = RLock()
        self._counters = AutomationCounters()
        self._current_cycle = ""
        self._phase = "idle"
        self._last_error = ""
        self._last_action = "ready"

    def begin_cycle(self, cycle_id: str) -> None:
        with self._lock:
            self._counters.cycles += 1
            self._current_cycle = cycle_id
            self._phase = "planning"
            self._last_error = ""

    def set_phase(self, phase: str) -> None:
        with self._lock:
            self._phase = phase

    def record(self, status: str, action: str = "", error: str = "") -> None:
        with self._lock:
            if hasattr(self._counters, status):
                setattr(self._counters, status, getattr(self._counters, status) + 1)
            if action:
                self._last_action = action
            if error:
                self._last_error = error[:500]

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                **asdict(self._counters),
                "cycle_id": self._current_cycle,
                "phase": self._phase,
                "last_action": self._last_action,
                "last_error": self._last_error,
            }
