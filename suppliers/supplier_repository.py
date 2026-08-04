from __future__ import annotations

import json
from typing import Any

from infrastructure.database.engine import utcnow
from suppliers.supplier_score import SupplierScore


class SupplierScoreRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, score: SupplierScore) -> None:
        self.db.execute(
            "INSERT INTO supplier_scores(supplier_id,score,risk_level,metrics_json,updated_at) VALUES(?,?,?,?,?) "
            "ON CONFLICT(supplier_id) DO UPDATE SET score=excluded.score,risk_level=excluded.risk_level,metrics_json=excluded.metrics_json,updated_at=excluded.updated_at",
            (score.supplier_id, score.score, score.risk_level, json.dumps(score.metrics, ensure_ascii=False), utcnow()),
        )

    def get(self, supplier_id: str) -> dict[str, Any] | None:
        return self.db.query_one("SELECT * FROM supplier_scores WHERE supplier_id=?", (supplier_id,))
