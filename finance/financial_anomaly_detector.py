from __future__ import annotations

from dataclasses import asdict,dataclass
from analytics.anomaly.base import RobustAnomalyDetector

@dataclass(frozen=True,slots=True)
class FinancialAnomalyAssessment:
    metric: str
    result: dict[str,object]
    estimated_impact_cad: float
    recommended_action: str
    def as_dict(self): return asdict(self)

class FinancialAnomalyDetector(RobustAnomalyDetector):
    def inspect(self,history: list[float],current: float) -> dict[str,object]: return self.assess("financial",history,current).result
    def assess(self,metric: str,history: list[float],current: float,*,exposure_cad: float=0) -> FinancialAnomalyAssessment:
        result=self.detect(history,current); action="none" if not result.anomalous else "freeze_period" if result.severity=="critical" else "review_transactions"
        impact=round(abs(current-result.center)*max(1,exposure_cad),2) if exposure_cad else round(abs(current-result.center),2)
        return FinancialAnomalyAssessment(metric,result.as_dict(),impact,action)
