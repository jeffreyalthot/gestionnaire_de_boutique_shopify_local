from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class CustomerConsent:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, *, customer_id: str, purpose: str, granted: bool, source: str,
               evidence: dict[str, Any] | None = None, expires_at: str | None = None) -> str:
        identifier = str(uuid4())
        recorded = datetime.now(timezone.utc).isoformat()
        evidence_json = json.dumps(evidence or {}, ensure_ascii=True, sort_keys=True, separators=(",", ":"), default=str)
        digest = hashlib.sha256(evidence_json.encode("utf-8")).hexdigest()
        self.db.execute(
            "INSERT INTO customer_consents(id,customer_id,purpose,granted,source,evidence_hash,recorded_at,expires_at) VALUES(?,?,?,?,?,?,?,?)",
            (identifier, customer_id, purpose, int(granted), source[:100], digest, recorded, expires_at),
        )
        return identifier

    def current(self, customer_id: str, purpose: str) -> bool:
        row = self.db.query_one(
            "SELECT granted,expires_at FROM customer_consents WHERE customer_id=? AND purpose=? ORDER BY recorded_at DESC LIMIT 1",
            (customer_id, purpose),
        )
        if not row or not bool(row["granted"]):
            return False
        expires = row.get("expires_at")
        return not expires or str(expires) > datetime.now(timezone.utc).isoformat()
