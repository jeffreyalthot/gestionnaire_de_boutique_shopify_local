from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class InventoryProjection:
    initial: int
    on_hand: int
    reserved: int
    damaged: int
    available: int
    applied_events: int
    ignored_events: tuple[str,...]
    def as_dict(self):return asdict(self)

class InventoryEventProjector:
    def project(self,initial: int,events: list[dict[str,object]]) -> int:return self.replay(initial,events).available
    def replay(self,initial: int,events: list[dict[str,object]]) -> InventoryProjection:
        on_hand=max(0,int(initial));reserved=damaged=0;ignored=[];seen=set();applied=0
        for event in events:
            ident=str(event.get("id",event.get("event_id","")))
            if ident and ident in seen:ignored.append(ident);continue
            if ident:seen.add(ident)
            kind=str(event.get("type",""));amount=max(0,int(event.get("quantity",0) or 0))
            if kind in {"received","adjusted_up","returned"}:on_hand+=amount
            elif kind in {"sold","adjusted_down"}:on_hand=max(0,on_hand-amount)
            elif kind=="reserved":reserved+=amount
            elif kind=="released":reserved=max(0,reserved-amount)
            elif kind=="damaged":damaged+=amount
            else:ignored.append(ident or kind);continue
            applied+=1
        available=max(0,on_hand-reserved-damaged);return InventoryProjection(initial,on_hand,reserved,damaged,available,applied,tuple(ignored))
