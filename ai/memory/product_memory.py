from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ai.memory.long_term_memory import LongTermMemory


class ProductMemory(LongTermMemory):
    prefix = "product"

    def put(self, key: str, value: object) -> None:
        self.remember(f"{self.prefix}:{key}", value, tags=("product",))

    def get(self, key: str, default: Any = None) -> Any:
        return self.recall(f"{self.prefix}:{key}", default)

    def record_snapshot(self, product_id: str, snapshot: dict[str, object]) -> dict[str, object]:
        history = self.get(f"{product_id}:history", [])
        if not isinstance(history, list):
            history = []
        item = dict(snapshot)
        item["recorded_at"] = datetime.now(timezone.utc).isoformat()
        history.append(item)
        history = history[-100:]
        self.put(f"{product_id}:history", history)
        self.put(f"{product_id}:latest", item)
        return item

    def latest(self, product_id: str) -> dict[str, object] | None:
        value = self.get(f"{product_id}:latest")
        return dict(value) if isinstance(value, dict) else None

    def history(self, product_id: str, limit: int = 20) -> tuple[dict[str, object], ...]:
        value = self.get(f"{product_id}:history", [])
        return tuple(dict(item) for item in value[-max(1, int(limit)):] if isinstance(item, dict)) if isinstance(value, list) else ()
