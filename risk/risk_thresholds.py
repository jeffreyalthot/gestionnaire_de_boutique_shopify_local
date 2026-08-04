from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskThresholds:
    review: float=.35
    hold: float=.50
    block: float=.80

    def action(self, score: float) -> str:
        if score>=self.block: return "block"
        if score>=self.hold: return "hold"
        if score>=self.review: return "review"
        return "allow"
