from __future__ import annotations
import asyncio,time
from collections import defaultdict
class DomainRateLimiter:
    def __init__(self,requests_per_second: float=2,burst: int=2)->None:
        self.rate=requests_per_second; self.burst=burst; self._tokens=defaultdict(lambda:float(burst)); self._updated=defaultdict(time.monotonic); self._lock=asyncio.Lock()
    async def acquire(self,domain: str)->None:
        while True:
            async with self._lock:
                now=time.monotonic(); elapsed=now-self._updated[domain]; self._updated[domain]=now
                self._tokens[domain]=min(self.burst,self._tokens[domain]+elapsed*self.rate)
                if self._tokens[domain]>=1: self._tokens[domain]-=1; return
                wait=(1-self._tokens[domain])/self.rate
            await asyncio.sleep(wait)
