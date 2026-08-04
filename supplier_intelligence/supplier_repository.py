from __future__ import annotations
from threading import RLock
from supplier_intelligence.supplier_profile import SupplierProfile

class SupplierRepository:
    def __init__(self) -> None:self._items={};self._lock=RLock()
    def save(self,p: SupplierProfile) -> None:
        if not p.supplier_id:raise ValueError("supplier_id requis")
        with self._lock:self._items[p.supplier_id]=p
    def get(self,supplier_id: str):
        with self._lock:return self._items.get(supplier_id)
    def delete(self,supplier_id: str) -> bool:
        with self._lock:return self._items.pop(supplier_id,None) is not None
    def list(self,status: str|None=None):
        with self._lock:return tuple(sorted((x for x in self._items.values() if status is None or x.status==status),key=lambda x:(-x.score,x.supplier_id)))
    def search(self,text: str):
        query=text.casefold()
        return tuple(item for item in self.list() if query in item.supplier_id.casefold() or query in item.legal_name.casefold())
    def stats(self):
        rows=self.list();return {"total":len(rows),"by_status":{status:sum(x.status==status for x in rows) for status in sorted({x.status for x in rows})}}
