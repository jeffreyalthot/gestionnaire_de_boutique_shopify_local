from __future__ import annotations

import hashlib
import json
from typing import Any


def idempotency_key(namespace: str, payload: dict[str, Any]) -> str:
    material = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(f"{namespace}:{material}".encode("utf-8")).hexdigest()


class IdempotentAction:
    def __init__(self, db: Any) -> None:
        self.db = db

    def completed(self, key: str) -> bool:
        return bool(self.db.scalar(
            "SELECT 1 FROM automation_actions WHERE idempotency_key=? AND status='completed'", (key,), default=0
        ))
