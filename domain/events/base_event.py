from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class DomainEvent:
    topic: str
    payload: dict[str, object]
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    correlation_id: str = ""
    causation_id: str = ""
    source: str = "domain"

    def __post_init__(self) -> None:
        topic = str(self.topic).strip().lower()
        if not topic or "." not in topic or len(topic) > 160:
            raise ValueError("topic de domaine invalide")
        if not isinstance(self.payload, dict):
            raise TypeError("payload événement invalide")
        body = json.dumps(self.payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
        if len(body) > 1_000_000:
            raise ValueError("payload événement trop volumineux")
        object.__setattr__(self, "topic", topic)
        object.__setattr__(self, "version", max(1, int(self.version)))
        if self.occurred_at.tzinfo is None:
            object.__setattr__(self, "occurred_at", self.occurred_at.replace(tzinfo=timezone.utc))
        else:
            object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(timezone.utc))

    @property
    def aggregate(self) -> str:
        return self.topic.split(".", 1)[0]

    @property
    def action(self) -> str:
        return self.topic.split(".", 1)[1]

    @property
    def fingerprint(self) -> str:
        body = json.dumps(
            {"topic": self.topic, "payload": self.payload, "version": self.version},
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()[:24]

    @property
    def event_hash(self) -> str:
        body = json.dumps(
            {
                "id": self.id,
                "occurred_at": self.occurred_at.isoformat(),
                "fingerprint": self.fingerprint,
                "correlation_id": self.correlation_id,
                "causation_id": self.causation_id,
                "source": self.source,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["occurred_at"] = self.occurred_at.astimezone(timezone.utc).isoformat()
        data["fingerprint"] = self.fingerprint
        data["event_hash"] = self.event_hash
        data["aggregate"] = self.aggregate
        data["action"] = self.action
        return data

    def caused_by(self, event: "DomainEvent") -> "DomainEvent":
        return replace(
            self,
            correlation_id=event.correlation_id or event.id,
            causation_id=event.id,
        )

    @classmethod
    def create(
        cls,
        aggregate: str,
        action: str,
        payload: Mapping[str, Any],
        **metadata: Any,
    ) -> "DomainEvent":
        return cls(topic=f"{aggregate}.{action}", payload=dict(payload), **metadata)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DomainEvent":
        occurred = datetime.fromisoformat(
            str(data.get("occurred_at") or datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00")
        )
        return cls(
            topic=str(data["topic"]),
            payload=dict(data.get("payload", {})),
            id=str(data.get("id") or uuid4()),
            occurred_at=occurred,
            version=int(data.get("version", 1)),
            correlation_id=str(data.get("correlation_id", "")),
            causation_id=str(data.get("causation_id", "")),
            source=str(data.get("source", "domain")),
        )
