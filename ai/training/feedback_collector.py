from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class FeedbackRecord:
    decision_id: str
    outcome: float
    source: str
    note: str
    recorded_at: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class FeedbackCollector:
    def __init__(self, db: Database) -> None:
        self.db = db

    def record(self, decision_id: str, outcome: float, *, source: str = "operator", note: str = "") -> None:
        if not decision_id:
            raise ValueError("decision_id is required")
        value = float(outcome)
        updated = self.db.execute("UPDATE ai_decisions SET outcome=? WHERE id=?", (value, decision_id))
        record = FeedbackRecord(
            decision_id=decision_id,
            outcome=value,
            source=str(source),
            note=str(note)[:1000],
            recorded_at=datetime.now(timezone.utc).isoformat(),
        )
        self.db.set_value(f"ai-feedback:{decision_id}", record.as_dict())
        self.db.insert_audit("ai.feedback.recorded", source, {**record.as_dict(), "decision_found": bool(updated)})

    def get(self, decision_id: str) -> FeedbackRecord | None:
        payload = self.db.get_value(f"ai-feedback:{decision_id}")
        if not isinstance(payload, dict):
            return None
        return FeedbackRecord(
            decision_id=str(payload.get("decision_id", decision_id)),
            outcome=float(payload.get("outcome", 0.0)),
            source=str(payload.get("source", "")),
            note=str(payload.get("note", "")),
            recorded_at=str(payload.get("recorded_at", "")),
        )

    def pending_decisions(self, limit: int = 100) -> tuple[dict[str, Any], ...]:
        rows = self.db.query(
            "SELECT id,decision_type,entity_id,confidence,action,features_json,created_at "
            "FROM ai_decisions WHERE outcome IS NULL ORDER BY created_at LIMIT ?",
            (max(1, min(int(limit), 1000)),),
        )
        return tuple(rows)
