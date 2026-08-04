from collections import defaultdict, deque
from time import time


class VelocityDetector:
    def __init__(self, window_seconds: int=3600, limit: int=3) -> None:
        self.window=max(1,window_seconds); self.limit=max(1,limit); self._events=defaultdict(deque)
    def observe(self, identity: str, now: float | None=None) -> tuple[int,bool]:
        now=time() if now is None else now; q=self._events[identity]
        while q and q[0]<now-self.window: q.popleft()
        q.append(now); return len(q),len(q)>self.limit
