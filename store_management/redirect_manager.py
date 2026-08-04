from __future__ import annotations
from dataclasses import asdict,dataclass
from urllib.parse import urlparse

@dataclass(frozen=True,slots=True)
class RedirectPlan:
    source: str
    target: str
    status_code: int
    external: bool
    safe: bool
    reason: str
    def as_dict(self):return asdict(self)

class RedirectManager:
    def normalize(self,source: str,target: str) -> tuple[str,str]:
        plan=self.plan(source,target)
        if not plan.safe:raise ValueError("boucle de redirection" if plan.reason=="redirect_loop" else plan.reason)
        return plan.source,plan.target
    def plan(self,source: str,target: str,*,status_code: int=301,allow_external: bool=False) -> RedirectPlan:
        source_value="/"+str(source).strip().lstrip("/");raw_target=str(target).strip();external=bool(urlparse(raw_target).scheme);target_value=raw_target if external else "/"+raw_target.lstrip("/")
        reason="allowed";safe=True
        if source_value==target_value:safe=False;reason="redirect_loop"
        elif status_code not in {301,302,307,308}:safe=False;reason="unsupported_status"
        elif external and not allow_external:safe=False;reason="external_redirect_blocked"
        return RedirectPlan(source_value,target_value,status_code,external,safe,reason)
    def detect_cycles(self,redirects: list[tuple[str,str]]) -> tuple[tuple[str,...],...]:
        graph={source:target for source,target in redirects};cycles=[]
        for start in graph:
            seen=[];current=start
            while current in graph and current not in seen:
                seen.append(current);current=graph[current]
            if current in seen:
                cycle=tuple(seen[seen.index(current):]+[current])
                if cycle not in cycles:cycles.append(cycle)
        return tuple(cycles)
