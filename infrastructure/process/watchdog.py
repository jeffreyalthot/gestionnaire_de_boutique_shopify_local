from __future__ import annotations
import time
class Watchdog:
    def __init__(self,timeout_seconds: float=60)->None: self.timeout=timeout_seconds; self.last=time.monotonic(); self.reason=''
    def feed(self,reason: str='')->None: self.last=time.monotonic(); self.reason=reason
    def expired(self)->bool: return time.monotonic()-self.last>self.timeout
