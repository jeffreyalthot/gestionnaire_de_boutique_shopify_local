from dataclasses import dataclass
from collections.abc import Awaitable,Callable
@dataclass(slots=True)
class ScheduledJob:
    name: str
    interval_seconds: float
    action: Callable[[],Awaitable[None]]
    run_immediately: bool=True
class JobRegistry:
    def __init__(self) -> None: self.jobs: dict[str,ScheduledJob]={}
    def register(self,job: ScheduledJob) -> None:
        if job.interval_seconds<=0: raise ValueError("Intervalle invalide.")
        self.jobs[job.name]=job
