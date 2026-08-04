from __future__ import annotations
import hashlib
from dataclasses import asdict,dataclass
from datetime import datetime,timezone

@dataclass(frozen=True,slots=True)
class RFQ:
    rfq_id: str
    sku: str
    quantity: int
    destination_country: str
    requirements: dict[str,object]
    status: str
    created_at: str
    expires_at: str
    idempotency_key: str
    def as_dict(self):return asdict(self)

class RFQBuilder:
    def build(self,*,sku: str,quantity: int,destination_country: str,requirements: dict[str,object]|None=None) -> dict[str,object]:return self.create(sku=sku,quantity=quantity,destination_country=destination_country,requirements=requirements).as_dict()
    def create(self,*,sku: str,quantity: int,destination_country: str,requirements: dict[str,object]|None=None,expires_at: str="") -> RFQ:
        sku=str(sku).strip().upper();quantity=int(quantity);country=str(destination_country).strip().upper();requirements=dict(requirements or {})
        if not sku or quantity<=0 or len(country)!=2:raise ValueError("RFQ invalide")
        key=hashlib.sha256(f"{sku}|{quantity}|{country}|{sorted(requirements.items())}".encode()).hexdigest();return RFQ(key[:16],sku,quantity,country,requirements,"draft",datetime.now(timezone.utc).isoformat(),expires_at,key)
