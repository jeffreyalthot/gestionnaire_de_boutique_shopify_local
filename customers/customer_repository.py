from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from customers.customer_profile import CustomerProfile


class CustomerRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, profile: CustomerProfile) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
            "INSERT INTO customer_profiles(customer_id,email_hash,country_code,language,lifetime_value_cad,risk_score,preferences_json,tags_json,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(customer_id) DO UPDATE SET email_hash=excluded.email_hash,country_code=excluded.country_code,language=excluded.language,lifetime_value_cad=excluded.lifetime_value_cad,risk_score=excluded.risk_score,preferences_json=excluded.preferences_json,tags_json=excluded.tags_json,updated_at=excluded.updated_at",
            (profile.customer_id, profile.email_hash, profile.country_code, profile.language,
             max(0.0, profile.lifetime_value_cad), max(0.0, min(1.0, profile.risk_score)),
             json.dumps(profile.preferences, ensure_ascii=False, default=str),
             json.dumps(sorted(set(profile.tags)), ensure_ascii=False), profile.created_at, now),
        )

    def get(self, customer_id: str) -> CustomerProfile | None:
        row = self.db.query_one("SELECT * FROM customer_profiles WHERE customer_id=?", (customer_id,))
        if not row:
            return None
        return CustomerProfile(
            customer_id=row["customer_id"], email_hash=row["email_hash"], country_code=row["country_code"],
            language=row["language"], lifetime_value_cad=float(row["lifetime_value_cad"]),
            risk_score=float(row["risk_score"]), preferences=json.loads(row["preferences_json"]),
            tags=tuple(json.loads(row["tags_json"])), created_at=row["created_at"], updated_at=row["updated_at"],
        )

    def list(self, limit: int = 100) -> list[CustomerProfile]:
        identifiers = self.db.query("SELECT customer_id FROM customer_profiles ORDER BY updated_at DESC LIMIT ?", (max(1, min(limit, 1000)),))
        return [profile for row in identifiers if (profile := self.get(str(row["customer_id"]))) is not None]
