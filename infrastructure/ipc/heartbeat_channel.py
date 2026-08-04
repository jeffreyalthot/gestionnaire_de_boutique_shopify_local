from __future__ import annotations
import time
class HeartbeatChannel:
    def __init__(self,timeout_seconds: float=10)->None: self.timeout=timeout_seconds; self.last=time.monotonic()
    def beat(self)->None: self.last=time.monotonic()
    def healthy(self)->bool: return time.monotonic()-self.last<=self.timeout
