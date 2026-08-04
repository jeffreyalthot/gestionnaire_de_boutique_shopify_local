from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import date

@dataclass(frozen=True,slots=True)
class PreorderDecision:
    allowed: bool
    reason: str
    release_date: str
    days_until_release: int
    quantity_limit: int
    deposit_percent: float
    def as_dict(self):return asdict(self)

class PreorderPolicy:
    def decide(self,*,release_date: date|None,supplier_confirmed: bool,enabled: bool=False) -> tuple[bool,str]:
        result=self.evaluate(release_date=release_date,supplier_confirmed=supplier_confirmed,enabled=enabled);return result.allowed,result.reason
    def evaluate(self,*,release_date: date|None,supplier_confirmed: bool,enabled: bool=False,supplier_available: int=0,reserved_preorders: int=0,maximum_days: int=180,deposit_percent: float=0) -> PreorderDecision:
        today=date.today();days=(release_date-today).days if release_date else -1;reason="allowed"
        if not enabled:reason="disabled"
        elif not supplier_confirmed:reason="supplier_unconfirmed"
        elif release_date is None or days<=0:reason="invalid_release_date"
        elif days>maximum_days:reason="release_too_far"
        elif supplier_available<=reserved_preorders:reason="capacity_exhausted"
        allowed=reason=="allowed";limit=max(0,int(supplier_available)-int(reserved_preorders)) if allowed else 0
        return PreorderDecision(allowed,reason,release_date.isoformat() if release_date else "",days,limit,max(0,min(100,float(deposit_percent))))
