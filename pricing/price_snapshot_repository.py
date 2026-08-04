from __future__ import annotations
from statistics import fmean,pstdev
from datetime import datetime,timezone
from pricing.price_history import PriceHistory
class PriceSnapshotRepository(PriceHistory):
    def volatility(self,entity_type: str,entity_id: str,limit: int=30) -> dict[str,object]:
        rows=self.series(entity_type,entity_id,limit);prices=[float(r.get("price_cad",0) or 0) for r in rows]
        if not prices:return {"samples":0,"mean_cad":0.0,"stdev_cad":0.0,"coefficient":0.0,"volatile":False}
        mean=fmean(prices);stdev=pstdev(prices) if len(prices)>1 else 0.0;coefficient=stdev/max(.01,mean)
        return {"samples":len(prices),"mean_cad":round(mean,2),"stdev_cad":round(stdev,2),"coefficient":round(coefficient,6),"volatile":coefficient>=.15}
    def stale(self,entity_type: str,entity_id: str,max_age_seconds: int) -> bool:
        row=self.latest(entity_type,entity_id)
        if not row:return True
        observed=datetime.fromisoformat(str(row["observed_at"]).replace("Z","+00:00"));return (datetime.now(timezone.utc)-observed).total_seconds()>max_age_seconds
    def change(self,entity_type: str,entity_id: str) -> dict[str,object]:
        rows=self.series(entity_type,entity_id,2)
        if len(rows)<2:return {"changed":False,"delta_cad":0.0,"delta_percent":0.0}
        current,previous=float(rows[0]["price_cad"]),float(rows[1]["price_cad"]);delta=current-previous
        return {"changed":delta!=0,"delta_cad":round(delta,2),"delta_percent":round(delta/max(.01,previous)*100,4)}
