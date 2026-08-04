from __future__ import annotations

from dataclasses import MISSING, asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(slots=True)
class QueueTask:
    id: str
    queue: str
    task_type: str
    payload: dict[str, Any]
    priority: int
    attempts: int
    max_attempts: int
    idempotency_key: str
    status: str = "pending"
    available_at: str = ""
    lease_until: str = ""
    worker_id: str = ""
    error: str = ""
    created_at: str = ""
    updated_at: str = ""
    schema_version: int = 2

    def __post_init__(self) -> None:
        self.id = str(self.id).strip()
        self.queue = str(self.queue).strip()
        self.task_type = str(self.task_type).strip()
        self.idempotency_key = str(self.idempotency_key).strip()
        if not all((self.id, self.queue, self.task_type, self.idempotency_key)):
            raise ValueError("queue_task_identity_invalid")
        if len(self.payload) > 10_000:
            raise ValueError("queue_task_payload_too_large")
        self.priority = max(-100, min(100, int(self.priority)))
        self.attempts = max(0, int(self.attempts))
        self.max_attempts = max(1, int(self.max_attempts))
        if self.attempts > self.max_attempts:
            raise ValueError("queue_task_attempts_invalid")
        now = datetime.now(timezone.utc).isoformat()
        self.created_at = self.created_at or now
        self.updated_at = self.updated_at or now

    @property
    def retryable(self) -> bool:
        return self.attempts < self.max_attempts and self.status not in {"completed", "cancelled", "dead"}

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "QueueTask":
        fields = cls.__dataclass_fields__
        kwargs: dict[str, Any] = {}
        for name, descriptor in fields.items():
            if name in value:
                kwargs[name] = value[name]
            elif descriptor.default is not MISSING:
                kwargs[name] = descriptor.default
            elif descriptor.default_factory is not MISSING:  # type: ignore[comparison-overlap]
                kwargs[name] = descriptor.default_factory()  # type: ignore[misc]
        return cls(**kwargs)
