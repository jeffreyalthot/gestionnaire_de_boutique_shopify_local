from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone

@dataclass(slots=True)
class WatchlistEntry:
    supplier_id: str
    reason: str
    severity: str="medium"
    created_at: str=""
    expires_at: str=""
    occurrences: int=1
    def __post_init__(self):
        if not self.created_at:self.created_at=datetime.now(timezone.utc).isoformat()

class SupplierWatchlist:
    def __init__(self) -> None:self._entries={}
    def add(self,supplier_id: str,reason: str,*,severity: str="medium",expires_at: str="") -> None:
        existing=self._entries.get(supplier_id)
        if existing:existing.reason=reason[:500];existing.severity=severity;existing.occurrences+=1;existing.expires_at=expires_at
        else:self._entries[supplier_id]=WatchlistEntry(supplier_id,reason[:500],severity,expires_at=expires_at)
    def remove(self,supplier_id: str) -> bool:return self._entries.pop(supplier_id,None) is not None
    def contains(self,supplier_id: str) -> bool:return supplier_id in self._entries
    def list(self) -> dict[str,str]:return {key:value.reason for key,value in self._entries.items()}
    def details(self):return tuple(asdict(value) for value in sorted(self._entries.values(),key=lambda x:(x.severity,x.supplier_id),reverse=True))
