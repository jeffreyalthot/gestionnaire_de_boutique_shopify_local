from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class MessageHistory:
    def __init__(self, db: Any) -> None:
        self.db = db

    def append(self, ticket_id: str, *, direction: str, channel: str, body_reference: str,
               metadata: dict[str, object] | None = None) -> None:
        key = f"ticket-history:{ticket_id}"
        history = list(self.db.get_value(key, []))
        history.append({"direction": direction, "channel": channel, "body_reference": body_reference,
                        "metadata": metadata or {}, "at": datetime.now(timezone.utc).isoformat()})
        self.db.set_value(key, history[-100:])

    def get(self, ticket_id: str) -> tuple[dict[str, object], ...]:
        return tuple(self.db.get_value(f"ticket-history:{ticket_id}", []))
