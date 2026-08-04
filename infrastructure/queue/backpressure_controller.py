from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class BackpressureDecision:
    accept: bool; ratio: float; delay_seconds: float; reason: str
class BackpressureController:
    def __init__(self,maximum_pending: int,soft_ratio: float=.8)->None: self.maximum=maximum_pending; self.soft=soft_ratio
    def decide(self,pending: int)->BackpressureDecision:
        ratio=pending/self.maximum if self.maximum else 1.0
        if ratio>=1: return BackpressureDecision(False,ratio,60,'capacity_exhausted')
        if ratio>=self.soft: return BackpressureDecision(True,ratio,min(30,(ratio-self.soft)*150),'soft_throttle')
        return BackpressureDecision(True,ratio,0,'normal')
