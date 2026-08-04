from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ai.memory.long_term_memory import LongTermMemory


class DecisionHistory(LongTermMemory):
    prefix = "decision"

    def put(self, key: str, value: object) -> None:
        self.remember(f"{self.prefix}:{key}", value, tags=("decision",))

    def get(self, key: str, default: Any = None) -> Any:
        return self.recall(f"{self.prefix}:{key}", default)

    def record_decision(
        self,
        decision_id: str,
        *,
        action: str,
        confidence: float,
        entity_id: str = "",
        features: dict[str, object] | None = None,
        outcome: float | None = None,
    ) -> dict[str, object]:
        item = {
            "decision_id": str(decision_id),
            "action": str(action),
            "confidence": max(0.0, min(1.0, float(confidence))),
            "entity_id": str(entity_id),
            "features": dict(features or {}),
            "outcome": outcome,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.put(decision_id, item)
        return item

    def update_outcome(self, decision_id: str, outcome: float) -> bool:
        item = self.get(decision_id)
        if not isinstance(item, dict):
            return False
        item["outcome"] = float(outcome)
        item["outcome_recorded_at"] = datetime.now(timezone.utc).isoformat()
        self.put(decision_id, item)
        return True

    def recent(self, limit: int = 100) -> tuple[dict[str, object], ...]:
        records = self.scan(f"{self.prefix}:", limit=limit)
        values = [record.value for record in records if isinstance(record.value, dict)]
        values.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
        return tuple(values[: max(1, int(limit))])

    def success_rate(self) -> float:
        outcomes = [item.get("outcome") for item in self.recent(1000)]
        numeric = [float(value) for value in outcomes if value is not None]
        return sum(value > 0 for value in numeric) / len(numeric) if numeric else 0.0
