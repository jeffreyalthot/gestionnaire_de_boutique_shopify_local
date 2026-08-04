from dataclasses import dataclass
from risk.risk_score import RiskScore
from risk.risk_thresholds import RiskThresholds


@dataclass(frozen=True, slots=True)
class RiskGateDecision:
    allowed: bool
    action: str
    score: RiskScore


class HighRiskOrderGate:
    def __init__(self, thresholds: RiskThresholds | None=None) -> None: self.thresholds=thresholds or RiskThresholds()
    def evaluate(self, score: RiskScore) -> RiskGateDecision:
        action=self.thresholds.action(score.score); return RiskGateDecision(action in {"allow","review"},action,score)
