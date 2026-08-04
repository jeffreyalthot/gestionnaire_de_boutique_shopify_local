from __future__ import annotations

from datetime import datetime, timezone
from os import getpid
from time import monotonic
from typing import Any

_STARTED = monotonic()
_LAST_HEARTBEAT = _STARTED
_HEARTBEAT_SEQUENCE = 0


def heartbeat() -> dict[str, Any]:
    global _LAST_HEARTBEAT, _HEARTBEAT_SEQUENCE
    _LAST_HEARTBEAT = monotonic()
    _HEARTBEAT_SEQUENCE += 1
    return liveness()


def liveness(*, stale_after_seconds: float = 120.0) -> dict[str, object]:
    now = monotonic()
    heartbeat_age = max(0.0, now - _LAST_HEARTBEAT)
    alive = heartbeat_age <= max(1.0, float(stale_after_seconds))
    return {
        "status": "alive" if alive else "stale",
        "ok": alive,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pid": getpid(),
        "uptime_seconds": round(now - _STARTED, 3),
        "heartbeat_age_seconds": round(heartbeat_age, 3),
        "heartbeat_sequence": _HEARTBEAT_SEQUENCE,
    }
