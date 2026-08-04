from __future__ import annotations

import json
from typing import Any

from catalog.discovery.product_candidate import ProductCandidate
from infrastructure.database.engine import utcnow


class CandidateRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, candidate: ProductCandidate, *, score: float = 0.0, status: str = "candidate") -> str:
        self.db.execute(
            "INSERT INTO products(id,supplier_product_id,title,category,supplier_id,currency,supplier_cost,status,score,data_json,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(supplier_product_id) DO UPDATE SET title=excluded.title,category=excluded.category,supplier_id=excluded.supplier_id,currency=excluded.currency,supplier_cost=excluded.supplier_cost,score=excluded.score,data_json=excluded.data_json,updated_at=excluded.updated_at",
            (candidate.source_id, candidate.source_id, candidate.title, candidate.category_id, candidate.supplier_id,
             candidate.currency, candidate.unit_cost, status, score, json.dumps(candidate.as_dict(), ensure_ascii=False, default=str), utcnow(), utcnow()),
        )
        return candidate.source_id
