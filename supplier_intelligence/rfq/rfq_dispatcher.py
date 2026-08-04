from __future__ import annotations
from hashlib import sha256
class RFQDispatcher:
    def plan(self,rfq: dict[str,object],supplier_ids: list[str],max_suppliers: int=5) -> tuple[dict[str,object],...]:
        if rfq.get("status") not in {"draft","approved"}:raise ValueError("RFQ non expédiable")
        unique=tuple(dict.fromkeys(str(s).strip() for s in supplier_ids if str(s).strip()))[:max(1,max_suppliers)]
        rows=[]
        for supplier in unique:
            key=sha256(f"{supplier}|{rfq.get('sku')}|{rfq.get('quantity')}|{rfq.get('destination_country')}".encode()).hexdigest()
            rows.append({"supplier_id":supplier,"rfq":dict(rfq),"status":"queued","idempotency_key":key,"priority":int(rfq.get("priority",100) or 100)})
        return tuple(rows)
