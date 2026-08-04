from __future__ import annotations


class RiskSegment:
    def classify(self, risk_score: float) -> tuple[str, float]:
        score = max(0.0, min(1.0, float(risk_score)))
        return ("blocked" if score >= 0.85 else ("review" if score >= 0.50 else "normal"), score)
