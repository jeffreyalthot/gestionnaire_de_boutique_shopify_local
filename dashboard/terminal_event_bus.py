from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock


@dataclass(frozen=True)
class TerminalEvent:
    at: str
    level: str
    message: str


class TerminalEventBus:
    def __init__(self, capacity: int = 100) -> None:
        self._events: deque[TerminalEvent] = deque(maxlen=max(1, capacity))
        self._lock = Lock()

    def publish(self, message: str, level: str = 'INFO') -> TerminalEvent:
        event = TerminalEvent(datetime.now(timezone.utc).isoformat(), level.upper(),
                              message.replace('\r', ' ').replace('\n', ' ')[:500])
        with self._lock:
            self._events.append(event)
        return event

    def latest(self, count: int = 10) -> tuple[TerminalEvent, ...]:
        with self._lock:
            return tuple(self._events)[-max(0, count):]
