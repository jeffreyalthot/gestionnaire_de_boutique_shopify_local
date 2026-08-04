from __future__ import annotations
from dataclasses import asdict,dataclass,field,replace
from datetime import datetime,timezone

@dataclass(frozen=True,slots=True)
class SupplierProfile:
    supplier_id: str
    legal_name: str=""
    score: float=0.0
    status: str="candidate"
    certifications: tuple[str,...]=field(default_factory=tuple)
    metrics: dict[str,float]=field(default_factory=dict)
    country_code: str=""
    capabilities: tuple[str,...]=field(default_factory=tuple)
    updated_at: str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    def as_dict(self):return asdict(self)
    def update(self,**changes: object) -> "SupplierProfile":
        if "score" in changes:changes["score"]=max(0,min(1,float(changes["score"])))
        changes["updated_at"]=datetime.now(timezone.utc).isoformat();return replace(self,**changes)
