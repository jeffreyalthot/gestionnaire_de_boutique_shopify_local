from time import monotonic


class AlertSuppression:
    def __init__(self, window_seconds: float=300) -> None: self.window=max(1,window_seconds); self._last={}
    def allow(self,key: str) -> bool:
        now=monotonic(); previous=self._last.get(key,0)
        if now-previous<self.window: return False
        self._last[key]=now; return True
