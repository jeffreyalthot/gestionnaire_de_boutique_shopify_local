from __future__ import annotations
import asyncio
from collections import deque
from copy import deepcopy
from typing import Any
from app.health_aggregator import HealthAggregator

class HealthRegistry(HealthAggregator):
    def __init__(self,history_size: int=60) -> None:
        super().__init__();self._history=deque(maxlen=max(1,history_size));self._lock=asyncio.Lock()
    async def collect(self) -> dict[str,Any]:
        async with self._lock:
            snapshot=await super().collect();self._history.append(deepcopy(snapshot));return snapshot
    def history(self,limit: int=20) -> tuple[dict[str,Any],...]:return tuple(deepcopy(list(self._history)[-max(1,limit):]))
    def trend(self) -> dict[str,object]:
        rows=list(self._history);return {"samples":len(rows),"healthy":sum(r.get("status")=="healthy" for r in rows),"degraded":sum(r.get("status")=="degraded" for r in rows),"unhealthy":sum(r.get("status")=="unhealthy" for r in rows),"last_status":rows[-1].get("status") if rows else "unknown"}
