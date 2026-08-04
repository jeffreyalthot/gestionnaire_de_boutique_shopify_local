from __future__ import annotations
from datetime import datetime,timezone
class OperationalSummaryReport:
    def __init__(self,db) -> None:self.db=db
    def generate(self) -> dict[str,object]:
        counts=self.db.counts();queue={str(r["status"]):int(r["count"]) for r in self.db.query("SELECT status,COUNT(*) count FROM tasks GROUP BY status")};orders=self.db.query_one("SELECT COUNT(*) count,COALESCE(SUM(revenue_cad),0) revenue,COALESCE(SUM(profit_cad),0) profit FROM orders") or {};alerts=int(self.db.scalar("SELECT COUNT(*) FROM automation_exceptions WHERE status IN ('open','retry')",default=0))
        return {"generated_at":datetime.now(timezone.utc).isoformat(),"counts":counts,"queue":queue,"orders":{"count":int(orders.get("count",0)),"revenue_cad":round(float(orders.get("revenue",0)),2),"profit_cad":round(float(orders.get("profit",0)),2)},"open_exceptions":alerts,"healthy":int(queue.get("dead",0))==0 and alerts==0}
