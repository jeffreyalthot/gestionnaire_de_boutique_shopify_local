from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from uuid import uuid4

from config.paths import LOG_DIR

_LOCK = RLock()


@dataclass(frozen=True, slots=True)
class Incident:
    incident_id: str
    timestamp: str
    kind: str
    severity: str
    detail: dict[str, object]
    correlation_id: str = ""

    def as_dict(self) -> dict[str, object]: return asdict(self)


class IncidentRecorder:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (LOG_DIR / "incidents.jsonl")

    def record(self, kind: str, detail: dict[str, object], *, severity: str = "error", correlation_id: str = "") -> Incident:
        incident = Incident(uuid4().hex, datetime.now(timezone.utc).isoformat(), str(kind), severity, dict(detail), correlation_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(incident.as_dict(), ensure_ascii=False, default=str, separators=(",", ":"))
        with _LOCK, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n"); handle.flush()
        return incident

    def recent(self, limit: int = 50) -> tuple[dict[str, object], ...]:
        if not self.path.exists(): return ()
        with _LOCK: lines = self.path.read_text(encoding="utf-8").splitlines()[-max(1, limit):]
        return tuple(json.loads(line) for line in lines if line.strip())


def record_incident(kind: str, detail: dict[str, object]) -> Path:
    recorder = IncidentRecorder(); recorder.record(kind, detail); return recorder.path
