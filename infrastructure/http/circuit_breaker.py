from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from time import monotonic
@dataclass(frozen=True,slots=True)
class CircuitSnapshot:
    state:str;failures:int;limit:int;reset_seconds:float;opened_for_seconds:float
class CircuitBreaker:
    def __init__(self,failures: int=5,reset_seconds: float=60,half_open_attempts: int=1) -> None:
        self.limit=max(1,int(failures));self.reset_seconds=max(.01,float(reset_seconds));self.half_open_attempts=max(1,int(half_open_attempts));self.count=0;self.opened_at=0.0;self._half_open_inflight=0;self._lock=RLock()
    @property
    def state(self) -> str:
        if self.count<self.limit:return "closed"
        return "half_open" if monotonic()-self.opened_at>=self.reset_seconds else "open"
    def allow(self) -> bool:
        with self._lock:
            state=self.state
            if state=="closed":return True
            if state=="open":return False
            if self._half_open_inflight>=self.half_open_attempts:return False
            self._half_open_inflight+=1;return True
    def success(self) -> None:
        with self._lock:self.count=0;self.opened_at=0.0;self._half_open_inflight=0
    def failure(self) -> None:
        with self._lock:
            self.count+=1;self._half_open_inflight=max(0,self._half_open_inflight-1)
            if self.count>=self.limit and not self.opened_at:self.opened_at=monotonic()
    def snapshot(self) -> CircuitSnapshot:
        with self._lock:return CircuitSnapshot(self.state,self.count,self.limit,self.reset_seconds,max(0.0,monotonic()-self.opened_at) if self.opened_at else 0.0)
