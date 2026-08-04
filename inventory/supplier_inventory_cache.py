from __future__ import annotations
from dataclasses import asdict,dataclass
from threading import RLock
from time import monotonic

@dataclass(frozen=True,slots=True)
class SupplierStockRecord:
    sku: str
    quantity: int
    age_seconds: float
    stale: bool
    source: str
    def as_dict(self):return asdict(self)

class SupplierInventoryCache:
    def __init__(self,ttl_seconds: float=300,maximum_entries: int=5000) -> None:self.ttl=max(1.,ttl_seconds);self.maximum=max(1,maximum_entries);self._data={};self._lock=RLock();self.hits=self.misses=self.evictions=0
    def set(self,sku: str,quantity: int,*,source: str="supplier") -> None:
        with self._lock:
            if sku not in self._data and len(self._data)>=self.maximum:self._data.pop(next(iter(self._data)));self.evictions+=1
            self._data[str(sku)]=(monotonic(),max(0,int(quantity)),source)
    def get(self,sku: str) -> int|None:
        record=self.inspect(sku);return None if record is None or record.stale else record.quantity
    def inspect(self,sku: str) -> SupplierStockRecord|None:
        with self._lock:
            row=self._data.get(sku)
            if row is None:self.misses+=1;return None
            age=monotonic()-row[0];stale=age>self.ttl
            if stale:self._data.pop(sku,None);self.misses+=1
            else:self.hits+=1
            return SupplierStockRecord(str(sku),row[1],round(age,3),stale,row[2])
    def stats(self):return {"entries":len(self._data),"hits":self.hits,"misses":self.misses,"evictions":self.evictions,"ttl_seconds":self.ttl}
