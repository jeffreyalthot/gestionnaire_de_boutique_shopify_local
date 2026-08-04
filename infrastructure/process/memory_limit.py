from __future__ import annotations
import psutil
class MemoryLimit:
    def __init__(self,max_rss_mb: float)->None: self.max=max_rss_mb
    def snapshot(self)->dict[str,float|bool]:
        rss=psutil.Process().memory_info().rss/1048576
        return {'rss_mb':round(rss,2),'max_rss_mb':self.max,'ok':rss<=self.max,'ratio':rss/self.max if self.max else 1.0}
