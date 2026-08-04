from __future__ import annotations
from datetime import datetime,timezone
from typing import Any
from customers.customer_consent import CustomerConsent
class ConsentLedger(CustomerConsent):
    def current_record(self,customer_id: str,purpose: str) -> dict[str,Any] | None:
        return self.db.query_one("SELECT * FROM customer_consents WHERE customer_id=? AND purpose=? ORDER BY recorded_at DESC LIMIT 1",(customer_id,purpose))
    def revoke(self,customer_id: str,purpose: str,source: str="operator",reason: str="") -> str:
        return self.record(customer_id=customer_id,purpose=purpose,granted=False,source=source,evidence={"reason":reason,"revoked_at":datetime.now(timezone.utc).isoformat()})
    def active_purposes(self,customer_id: str) -> tuple[str,...]:
        rows=self.db.query("SELECT DISTINCT purpose FROM customer_consents WHERE customer_id=?",(customer_id,));return tuple(sorted(str(r["purpose"]) for r in rows if self.current(customer_id,str(r["purpose"]))))
    def audit(self,customer_id: str) -> dict[str,object]:
        rows=self.db.query("SELECT purpose,granted,source,recorded_at,expires_at FROM customer_consents WHERE customer_id=? ORDER BY recorded_at",(customer_id,));return {"customer_id":customer_id,"records":rows,"active_purposes":self.active_purposes(customer_id),"record_count":len(rows)}
