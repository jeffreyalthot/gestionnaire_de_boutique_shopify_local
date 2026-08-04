from dataclasses import dataclass
from time import monotonic
@dataclass(slots=True)
class DashboardState:
    started_at: float
    last_refresh: float=0
    def uptime_seconds(self) -> float: return max(0,monotonic()-self.started_at)
