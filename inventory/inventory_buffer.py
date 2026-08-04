from __future__ import annotations
import math
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class InventoryBufferResult:
    cycle_stock: float
    safety_stock: float
    total_buffer: int
    service_factor: float
    lead_time_days: float
    def as_dict(self):return asdict(self)

class InventoryBuffer:
    def calculate(self,*,daily_demand: float,lead_time_days: float,demand_stddev: float=0.0,service_factor: float=1.65) -> int:return self.evaluate(daily_demand=daily_demand,lead_time_days=lead_time_days,demand_stddev=demand_stddev,service_factor=service_factor).total_buffer
    def evaluate(self,*,daily_demand: float,lead_time_days: float,demand_stddev: float=0.0,service_factor: float=1.65,lead_time_stddev: float=0) -> InventoryBufferResult:
        demand=max(0,float(daily_demand));lead=max(0,float(lead_time_days));demand_sd=max(0,float(demand_stddev));lead_sd=max(0,float(lead_time_stddev));factor=max(0,float(service_factor));cycle=demand*lead;safety=factor*math.sqrt(lead*demand_sd**2+(demand**2)*(lead_sd**2));return InventoryBufferResult(round(cycle,4),round(safety,4),int(math.ceil(cycle+safety)),factor,lead)
