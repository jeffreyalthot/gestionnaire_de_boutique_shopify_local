from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ai.memory.long_term_memory import LongTermMemory


class SupplierMemory(LongTermMemory):
    prefix = "supplier"

    def put(self, key: str, value: object) -> None:
        self.remember(f"{self.prefix}:{key}", value, tags=("supplier",))

    def get(self, key: str, default: Any = None) -> Any:
        return self.recall(f"{self.prefix}:{key}", default)

    def record_assessment(self, supplier_id: str, assessment: dict[str, object]) -> dict[str, object]:
        item = dict(assessment)
        item["assessed_at"] = datetime.now(timezone.utc).isoformat()
        history = self.get(f"{supplier_id}:assessments", [])
        if not isinstance(history, list):
            history = []
        history.append(item)
        self.put(f"{supplier_id}:assessments", history[-100:])
        self.put(f"{supplier_id}:latest", item)
        return item

    def latest(self, supplier_id: str) -> dict[str, object] | None:
        value = self.get(f"{supplier_id}:latest")
        return dict(value) if isinstance(value, dict) else None

    def risk_trend(self, supplier_id: str, limit: int = 10) -> float:
        history = self.get(f"{supplier_id}:assessments", [])
        scores = [float(item.get("risk_score", 0.0)) for item in history[-max(2, int(limit)):] if isinstance(item, dict)] if isinstance(history, list) else []
        return scores[-1] - scores[0] if len(scores) >= 2 else 0.0
