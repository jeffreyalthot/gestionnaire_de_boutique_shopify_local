from __future__ import annotations
from collections import deque
class AdaptiveTimeout:
    def __init__(self,minimum: float=5,maximum: float=60,window: int=20,multiplier: float=2)->None:
        self.minimum=minimum; self.maximum=maximum; self.multiplier=multiplier; self.samples=deque(maxlen=window)
    def observe(self,seconds: float)->None:
        if seconds>=0: self.samples.append(seconds)
    def value(self)->float:
        if not self.samples: return self.minimum
        ordered=sorted(self.samples); p95=ordered[min(len(ordered)-1,round((len(ordered)-1)*.95))]
        return max(self.minimum,min(self.maximum,p95*self.multiplier))
