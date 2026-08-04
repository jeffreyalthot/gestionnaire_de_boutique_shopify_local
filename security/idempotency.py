from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from threading import RLock
from typing import Any
from domain.value_objects.idempotency_key import build_idempotency_key
@dataclass(frozen=True,slots=True)
class IdempotencyRecord:
    key:str;result:Any;created_at:datetime;expires_at:datetime
class IdempotencyRegistry:
    def __init__(self,ttl_seconds: int=86400,max_entries: int=10000) -> None:self.ttl=max(1,int(ttl_seconds));self.max_entries=max(1,int(max_entries));self._records={};self._lock=RLock()
    def _purge(self,now: datetime) -> None:
        for key in [k for k,v in self._records.items() if v.expires_at<=now]:self._records.pop(key,None)
        if len(self._records)>self.max_entries:
            for key,_ in sorted(self._records.items(),key=lambda item:item[1].created_at)[:len(self._records)-self.max_entries]:self._records.pop(key,None)
    def reserve(self,key: str,result: Any=None) -> bool:
        now=datetime.now(timezone.utc)
        with self._lock:
            self._purge(now)
            if key in self._records:return False
            self._records[key]=IdempotencyRecord(key,result,now,now+timedelta(seconds=self.ttl));return True
    def complete(self,key: str,result: Any) -> None:
        now=datetime.now(timezone.utc)
        with self._lock:self._records[key]=IdempotencyRecord(key,result,now,now+timedelta(seconds=self.ttl));self._purge(now)
    def get(self,key: str,default: Any=None) -> Any:
        now=datetime.now(timezone.utc)
        with self._lock:self._purge(now);record=self._records.get(key);return record.result if record else default
    def snapshot(self) -> dict[str,object]:
        with self._lock:return {"entries":len(self._records),"ttl_seconds":self.ttl,"max_entries":self.max_entries}
__all__=["build_idempotency_key","IdempotencyRegistry","IdempotencyRecord"]
