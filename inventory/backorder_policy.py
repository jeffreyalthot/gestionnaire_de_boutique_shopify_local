from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class BackorderDecision:
    allowed: bool
    reason: str
    shortage: int
    supplier_available: int
    lead_time_days: float
    promised_days: int
    maximum_orders: int
    def as_dict(self):return asdict(self)

class BackorderPolicy:
    def decide(self,*,shortage: int,supplier_available: int,lead_time_days: float,enabled: bool=False) -> tuple[bool,str]:
        result=self.evaluate(shortage=shortage,supplier_available=supplier_available,lead_time_days=lead_time_days,enabled=enabled);return result.allowed,result.reason
    def evaluate(self,*,shortage: int,supplier_available: int,lead_time_days: float,enabled: bool=False,current_backorders: int=0,maximum_backorders: int=100,maximum_lead_time_days: float=30) -> BackorderDecision:
        shortage=int(shortage);available=max(0,int(supplier_available));lead=max(0,float(lead_time_days));reason="allowed"
        if not enabled:reason="disabled"
        elif shortage<=0:reason="no_shortage"
        elif available<shortage:reason="supplier_unavailable"
        elif lead>maximum_lead_time_days:reason="lead_time_too_long"
        elif current_backorders+shortage>maximum_backorders:reason="backorder_limit"
        allowed=reason=="allowed";return BackorderDecision(allowed,reason,shortage,available,lead,int(math.ceil(lead+3)) if allowed else 0,maximum_backorders)

import math
