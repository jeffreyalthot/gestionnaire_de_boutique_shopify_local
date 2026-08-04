from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone

@dataclass(slots=True)
class BlacklistEntry:
    supplier_id: str
    reason: str
    added_at: str
    actor: str
    permanent: bool=True
    review_after: str=""
    evidence: tuple[str,...]=()

class SupplierBlacklist:
    def __init__(self) -> None:self._entries: dict[str,BlacklistEntry]={}
    def add(self,supplier_id: str,reason: str,*,actor: str="system",permanent: bool=True,review_after: str="",evidence: tuple[str,...]=()) -> None:
        supplier_id=str(supplier_id).strip()
        if not supplier_id or not reason.strip():raise ValueError("fournisseur et raison requis")
        self._entries[supplier_id]=BlacklistEntry(supplier_id,reason[:500],datetime.now(timezone.utc).isoformat(),actor,permanent,review_after,tuple(evidence))
    def remove(self,supplier_id: str,*,authorized: bool) -> None:
        if not authorized:raise PermissionError("autorisation requise")
        self._entries.pop(supplier_id,None)
    def blocked(self,supplier_id: str) -> bool:return supplier_id in self._entries
    def get(self,supplier_id: str):
        entry=self._entries.get(supplier_id);return asdict(entry) if entry else None
    def list(self):return tuple(asdict(entry) for entry in sorted(self._entries.values(),key=lambda x:x.added_at,reverse=True))
