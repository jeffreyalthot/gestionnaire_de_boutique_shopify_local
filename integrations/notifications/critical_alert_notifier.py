from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock


@dataclass(frozen=True, slots=True)
class CriticalNotification:
    fingerprint: str
    message: str
    delivered: bool
    suppressed: bool
    occurrences: int
    created_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CriticalAlertNotifier:
    def __init__(self, service, maximum_fingerprints: int = 1_000) -> None:
        self.service = service
        self.maximum_fingerprints = max(10, int(maximum_fingerprints))
        self._occurrences: dict[str, int] = {}
        self._lock = RLock()

    def send(self, message: str, *, context: dict[str, object] | None = None, repeat_every: int = 10) -> CriticalNotification:
        text = " ".join(str(message).split())[:1000]
        if not text:
            raise ValueError("Message critique vide")
        fingerprint = hashlib.sha256((text + repr(sorted((context or {}).items()))).encode()).hexdigest()[:20]
        with self._lock:
            occurrences = self._occurrences.get(fingerprint, 0) + 1
            self._occurrences[fingerprint] = occurrences
            if len(self._occurrences) > self.maximum_fingerprints:
                self._occurrences.pop(next(iter(self._occurrences)), None)
        suppressed = occurrences > 1 and occurrences % max(1, int(repeat_every)) != 0
        delivered = False
        if not suppressed:
            self.service.critical(text)
            delivered = True
        return CriticalNotification(fingerprint, text, delivered, suppressed, occurrences, datetime.now(timezone.utc).isoformat())

    def notify(self, message: str) -> None:
        self.send(message)
