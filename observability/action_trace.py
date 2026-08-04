from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from time import monotonic
from uuid import uuid4


@dataclass(slots=True)
class ActionTrace:
    name: str
    started: float = field(default_factory=monotonic)
    attributes: dict[str, object] = field(default_factory=dict)
    status: str = "running"
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    parent_id: str | None = None
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at: str | None = None
    duration_ms: float | None = None
    error: str | None = None

    def finish(self, status: str = "ok", *, error: BaseException | str | None = None) -> float:
        self.status = status; self.finished_at = datetime.now(timezone.utc).isoformat()
        self.duration_ms = round((monotonic() - self.started) * 1000, 3)
        if error is not None: self.error = str(error)[:1000]
        return self.duration_ms

    def child(self, name: str, **attributes: object) -> "ActionTrace":
        return ActionTrace(name, attributes=attributes, parent_id=self.trace_id)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def __enter__(self) -> "ActionTrace": return self
    def __exit__(self, exc_type, exc, tb) -> None: self.finish("error" if exc else "ok", error=exc)
