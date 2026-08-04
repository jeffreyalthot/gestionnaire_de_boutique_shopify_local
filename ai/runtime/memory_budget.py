from __future__ import annotations
from dataclasses import dataclass
import os, psutil

@dataclass(frozen=True,slots=True)
class MemorySnapshot:
    rss_mb: float
    limit_mb: int
    available_mb: float
    within_budget: bool

class MemoryBudget:
    def __init__(self,limit_mb: int) -> None:
        self.limit_mb=limit_mb; self.process=psutil.Process(os.getpid())
    def snapshot(self) -> MemorySnapshot:
        rss=self.process.memory_info().rss/(1024*1024)
        return MemorySnapshot(round(rss,2),self.limit_mb,round(max(0,self.limit_mb-rss),2),rss<=self.limit_mb)
    def require(self,reserve_mb: float=0) -> None:
        snap=self.snapshot()
        if snap.rss_mb+reserve_mb>self.limit_mb:
            raise MemoryError(f"Budget mémoire dépassé: {snap.rss_mb:.1f}+{reserve_mb:.1f}>{self.limit_mb} Mo")
