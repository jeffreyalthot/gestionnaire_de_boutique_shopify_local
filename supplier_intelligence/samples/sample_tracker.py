from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from datetime import datetime,timezone

class SampleTracker:
    TRANSITIONS={"planned":{"ordered","cancelled"},"ordered":{"shipped","cancelled"},"shipped":{"delivered","lost"},"delivered":{"passed","failed","quarantined"},"quarantined":{"passed","failed"}}
    def __init__(self) -> None:self._items={};self._history=defaultdict(list)
    def update(self,sample_id: str,status: str,tracking: str="",*,detail: dict[str,object]|None=None) -> None:
        sample_id=str(sample_id).strip();status=str(status).strip().lower()
        if not sample_id:raise ValueError("sample_id requis")
        current=str(self._items.get(sample_id,{}).get("status","planned"))
        if sample_id in self._items and status!=current and status not in self.TRANSITIONS.get(current,set()):raise ValueError(f"transition invalide: {current}->{status}")
        row={"sample_id":sample_id,"status":status,"tracking":tracking,"detail":dict(detail or {}),"updated_at":datetime.now(timezone.utc).isoformat()};self._items[sample_id]=row;self._history[sample_id].append(deepcopy(row))
    def get(self,sample_id: str):return deepcopy(self._items.get(sample_id))
    def history(self,sample_id: str):return tuple(deepcopy(self._history.get(sample_id,())))
    def pending(self):return tuple(deepcopy(row) for row in self._items.values() if row["status"] not in {"passed","failed","cancelled","lost"})
