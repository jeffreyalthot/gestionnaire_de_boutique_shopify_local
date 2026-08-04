from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class DisputeMetrics:
    disputes: int
    orders: int
    dispute_rate: float
    won_rate: float
    average_resolution_days: float
    severity: str
    def as_dict(self):return asdict(self)

class SupplierDisputeHistory:
    def rate(self,disputes: int,orders: int) -> float:return self.summarize([{}]*max(0,disputes),orders=orders).dispute_rate
    def summarize(self,disputes: list[dict[str,object]],*,orders: int) -> DisputeMetrics:
        count=len(disputes);won=sum(str(row.get("outcome","")).lower() in {"won","refunded","resolved_buyer"} for row in disputes);days=[max(0,float(row.get("resolution_days",0) or 0)) for row in disputes if row.get("resolution_days") is not None];rate=count/max(1,int(orders));severity="low" if rate<.01 else "medium" if rate<.03 else "high" if rate<.08 else "critical"
        return DisputeMetrics(count,max(0,int(orders)),round(rate,4),round(won/max(1,count),4),round(sum(days)/max(1,len(days)),2),severity)
