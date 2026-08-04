from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class Schedule:
    name: str; interval_seconds: float; enabled: bool=True; heavy: bool=False
class ScheduleRegistry:
    def __init__(self)->None: self._schedules={}
    def register(self,schedule: Schedule)->None:
        if schedule.interval_seconds<=0 or schedule.name in self._schedules: raise ValueError('Planification invalide.')
        self._schedules[schedule.name]=schedule
    def enabled(self)->tuple[Schedule,...]: return tuple(s for s in self._schedules.values() if s.enabled)
