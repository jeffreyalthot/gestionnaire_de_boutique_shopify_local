from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import RLock


@dataclass(slots=True)
class Alert:
    severity: str
    message: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    fingerprint: str = ""
    occurrences: int = 1
    acknowledged: bool = False
    context: dict[str, object] = field(default_factory=dict)


class AlertManager:
    LEVELS = {"info": 10, "warning": 20, "error": 30, "critical": 40}

    def __init__(self, max_alerts: int = 100) -> None:
        self.max_alerts = max(1, int(max_alerts)); self._alerts: list[Alert] = []; self._lock = RLock()

    def add(self, severity: str, message: str, *, context: dict[str, object] | None = None, fingerprint: str | None = None) -> Alert:
        severity = severity if severity in self.LEVELS else "warning"
        fp = fingerprint or hashlib.sha256(f"{severity}:{message}".encode()).hexdigest()[:16]
        with self._lock:
            existing = next((alert for alert in self._alerts if alert.fingerprint == fp and not alert.acknowledged), None)
            if existing:
                existing.occurrences += 1; existing.created_at = datetime.now(timezone.utc).isoformat(); existing.context.update(context or {})
                return existing
            alert = Alert(severity, str(message)[:1000], fingerprint=fp, context=dict(context or {}))
            self._alerts = ([alert] + self._alerts)[:self.max_alerts]
            return alert

    def acknowledge(self, fingerprint: str) -> bool:
        with self._lock:
            alert = next((item for item in self._alerts if item.fingerprint == fingerprint), None)
            if not alert: return False
            alert.acknowledged = True; return True

    def snapshot(self, *, minimum_severity: str = "info", include_acknowledged: bool = True) -> list[dict[str, object]]:
        minimum = self.LEVELS.get(minimum_severity, 10)
        with self._lock:
            return [asdict(alert) for alert in self._alerts if self.LEVELS[alert.severity] >= minimum and (include_acknowledged or not alert.acknowledged)]
