from __future__ import annotations
from copy import deepcopy
from datetime import datetime,timezone

class FactoryAuditRegistry:
    def __init__(self) -> None:self._audits={}
    def record(self,supplier_id: str,audit: dict[str,object]) -> None:
        row=dict(audit);row.setdefault("audited_at",datetime.now(timezone.utc).isoformat());row.setdefault("score",0.);row.setdefault("status","completed");self._audits.setdefault(supplier_id,[]).append(row)
    def latest(self,supplier_id: str):
        rows=self._audits.get(supplier_id,[]);return deepcopy(rows[-1]) if rows else None
    def history(self,supplier_id: str,limit: int=20):return tuple(deepcopy(self._audits.get(supplier_id,[])[-max(1,limit):]))
    def trend(self,supplier_id: str) -> float:
        scores=[float(row.get("score",0) or 0) for row in self._audits.get(supplier_id,[])]
        return round(scores[-1]-scores[0],4) if len(scores)>1 else 0.
