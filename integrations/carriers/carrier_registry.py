from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class Carrier:
    code: str; name: str; tracking_template: str=''; score: float=0.5
class CarrierRegistry:
    def __init__(self)->None:self._items={}
    def register(self,carrier: Carrier)->None:self._items[carrier.code.upper()]=carrier
    def resolve(self,code: str)->Carrier|None:return self._items.get(code.upper())
    def best(self)->Carrier|None:return max(self._items.values(),key=lambda c:c.score,default=None)
