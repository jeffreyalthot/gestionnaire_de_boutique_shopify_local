from __future__ import annotations

import asyncio
import signal
from dataclasses import dataclass
from threading import Event, RLock
from time import monotonic
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class LifecycleSnapshot:
    state: str
    stop_requested: bool
    reason: str
    uptime_seconds: float
    transitions: int


class ApplicationLifecycle:
    """Machine d'état minimale et thread-safe pour le runtime canonique."""

    _ALLOWED = {
        "created": {"starting", "stopped"},
        "starting": {"running", "stopping", "failed"},
        "running": {"stopping", "failed"},
        "stopping": {"stopped", "failed"},
        "failed": {"stopping", "stopped"},
        "stopped": set(),
    }

    def __init__(self) -> None:
        self._state = "created"
        self._reason = ""
        self._started = monotonic()
        self._stop = Event()
        self._lock = RLock()
        self._transitions = 0

    def transition(self, state: str, *, reason: str = "") -> LifecycleSnapshot:
        state = str(state).lower()
        with self._lock:
            if state == self._state:
                return self.snapshot()
            if state not in self._ALLOWED.get(self._state, set()):
                raise RuntimeError(f"invalid_lifecycle_transition:{self._state}->{state}")
            self._state = state
            self._reason = str(reason)
            self._transitions += 1
            if state in {"stopping", "stopped", "failed"}:
                self._stop.set()
            return self.snapshot()

    def request_stop(self, reason: str = "requested") -> LifecycleSnapshot:
        with self._lock:
            self._reason = str(reason)
            self._stop.set()
            if self._state not in {"stopping", "stopped"} and "stopping" in self._ALLOWED.get(self._state, set()):
                self._state = "stopping"
                self._transitions += 1
            return self.snapshot()

    def wait(self, timeout: float | None = None) -> bool:
        return self._stop.wait(timeout)

    def snapshot(self) -> LifecycleSnapshot:
        with self._lock:
            return LifecycleSnapshot(self._state, self._stop.is_set(), self._reason, round(monotonic() - self._started, 3), self._transitions)


def install_signal_handlers(stop_callback: Callable[[], Any]) -> None:
    """Installe les signaux asyncio avec repli compatible Windows."""
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_callback)
        except (NotImplementedError, RuntimeError):
            signal.signal(sig, lambda *_args, callback=stop_callback: callback())
