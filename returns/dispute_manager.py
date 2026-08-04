from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class DisputeCase:
    id: str
    order_id: str
    status: str
    amount_cad: float
    due_at: str
    evidence_count: int


class DisputeManager:
    def __init__(self, db: Any) -> None:
        self.db = db

    def open(self, order_id: str, amount_cad: float, due_at: str, evidence_count: int = 0) -> DisputeCase:
        if amount_cad < 0:
            raise ValueError('Le montant du litige ne peut pas être négatif.')
        case = DisputeCase(str(uuid4()), order_id, 'open', round(amount_cad, 2), due_at, evidence_count)
        cases = list(self.db.get_value('returns:disputes', []))
        cases.append({**asdict(case), 'created_at': datetime.now(timezone.utc).isoformat()})
        self.db.set_value('returns:disputes', cases[-1000:])
        return case

    def list_open(self) -> list[dict[str, Any]]:
        return [case for case in self.db.get_value('returns:disputes', []) if case.get('status') == 'open']
