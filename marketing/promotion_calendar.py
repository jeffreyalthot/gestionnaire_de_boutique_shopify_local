from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import date,timedelta

@dataclass(frozen=True,slots=True)
class PromotionWindowDecision:
    available: bool
    start: str
    end: str
    blackout_dates: tuple[str,...]
    conflicts: tuple[tuple[str,str],...]
    duration_days: int
    reason: str
    def as_dict(self):return asdict(self)

class PromotionCalendar:
    def __init__(self,blackouts: set[date]|None=None) -> None:self.blackouts=set(blackouts or ())
    def available(self,start: date,end: date,existing: list[tuple[date,date]]) -> bool:return self.evaluate(start,end,existing).available
    def evaluate(self,start: date,end: date,existing: list[tuple[date,date]],*,maximum_days: int=31) -> PromotionWindowDecision:
        if end<start:return PromotionWindowDecision(False,start.isoformat(),end.isoformat(),(),(),0,"invalid_range")
        days=(end-start).days+1;blackouts=tuple(sorted(x.isoformat() for x in self.blackouts if start<=x<=end));conflicts=tuple((a.isoformat(),b.isoformat()) for a,b in existing if start<=b and end>=a);available=not blackouts and not conflicts and days<=maximum_days;reason="available" if available else "blackout" if blackouts else "conflict" if conflicts else "duration_exceeded"
        return PromotionWindowDecision(available,start.isoformat(),end.isoformat(),blackouts,conflicts,days,reason)
    def next_available(self,start: date,duration_days: int,existing: list[tuple[date,date]],*,search_days: int=365) -> tuple[date,date]|None:
        duration=max(1,duration_days)
        for offset in range(max(1,search_days)):
            candidate=start+timedelta(days=offset);end=candidate+timedelta(days=duration-1)
            if self.available(candidate,end,existing):return candidate,end
        return None
