from __future__ import annotations

from catalog.discovery.product_candidate import ProductCandidate


class OpportunityDetector:
    def evaluate(self, candidate: ProductCandidate, *, minimum_margin: float = 0.35) -> dict[str, object]:
        signals = candidate.signals
        demand = max(0.0, min(1.0, float(signals.get("demand", 0.5))))
        competition = max(0.0, min(1.0, float(signals.get("competition", 0.5))))
        supplier = max(0.0, min(1.0, float(signals.get("supplier", 0.5))))
        margin = max(0.0, min(1.0, float(signals.get("margin", 0.0))))
        return_risk = max(0.0, min(1.0, float(signals.get("return_risk", 0.2))))
        score = demand * 0.30 + (1 - competition) * 0.20 + supplier * 0.20 + margin * 0.25 + (1 - return_risk) * 0.05
        accepted = score >= 0.68 and margin >= minimum_margin
        return {"score": round(score, 4), "accepted": accepted, "reason": "qualified" if accepted else "below_threshold"}
