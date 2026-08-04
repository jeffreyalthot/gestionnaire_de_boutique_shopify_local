from __future__ import annotations

from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock


class DashboardController:
    def __init__(self, container, *, history_size: int = 120) -> None:
        self.container = container; self._history = deque(maxlen=max(1, history_size)); self._lock = RLock(); self.refresh_total = 0

    def snapshot(self) -> dict[str, object]:
        value = dict(self.container.dashboard_state()); value.setdefault("captured_at", datetime.now(timezone.utc).isoformat())
        with self._lock:
            self._history.append(deepcopy(value)); self.refresh_total += 1
        return value

    def history(self, limit: int = 20) -> tuple[dict[str, object], ...]:
        with self._lock: return tuple(deepcopy(list(self._history)[-max(1, limit):]))

    def changes(self) -> dict[str, tuple[object, object]]:
        with self._lock:
            if len(self._history) < 2: return {}
            previous, current = self._history[-2], self._history[-1]
        return {key: (previous.get(key), current.get(key)) for key in current.keys() | previous.keys() if previous.get(key) != current.get(key)}
