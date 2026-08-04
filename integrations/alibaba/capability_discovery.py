from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Any,Awaitable,Callable
@dataclass(frozen=True)
class CapabilityProbe:
    name: str; method: str; mutating: bool=False
class CapabilityDiscovery:
    def __init__(self,caller: Callable[[str],Any])->None:self.caller=caller
    async def discover(self,probes: list[CapabilityProbe])->dict[str,bool]:
        result={}
        for probe in probes:
            if probe.mutating: result[probe.name]=False; continue
            try:
                value=self.caller(probe.method)
                if asyncio.iscoroutine(value): value=await value
                result[probe.name]=value is not None
            except Exception: result[probe.name]=False
        return result
