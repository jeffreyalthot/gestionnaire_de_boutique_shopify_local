from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class NegotiationTarget:
    quoted_unit_cad: float
    benchmark_unit_cad: float
    target_unit_cad: float
    target_reduction_percent: float
    walk_away_unit_cad: float
    strategy: str
    def as_dict(self):return asdict(self)

class NegotiationPolicy:
    def target(self,*,quoted_unit_cad: float,benchmark_unit_cad: float,quantity: int) -> float:return self.plan(quoted_unit_cad=quoted_unit_cad,benchmark_unit_cad=benchmark_unit_cad,quantity=quantity).target_unit_cad
    def plan(self,*,quoted_unit_cad: float,benchmark_unit_cad: float,quantity: int,supplier_score: float=.5,maximum_reduction_percent: float=15) -> NegotiationTarget:
        quoted=max(0,float(quoted_unit_cad));benchmark=max(0,float(benchmark_unit_cad)) or quoted;volume=min(.12,max(0,quantity-10)/1000);quality_adjustment=max(-.03,min(.03,(float(supplier_score)-.5)*.06));reduction=min(maximum_reduction_percent/100,max(0,volume-quality_adjustment));base=min(quoted,benchmark);target=round(base*(1-reduction),2);walk=round(min(quoted,benchmark*1.1),2);strategy="volume" if volume>.03 else "benchmark" if benchmark<quoted else "relationship"
        return NegotiationTarget(quoted,benchmark,target,round(reduction*100,2),walk,strategy)
