from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConfidenceDecision:
    allowed: bool
    confidence: float
    required_confidence: float
    reason: str

def evaluate_confidence(confidence: float, minimum: float, *, financial: bool = False, irreversible: bool = False, risk_score: float = 0.0) -> ConfidenceDecision:
    score = min(1.0, max(0.0, float(confidence)))
    threshold = min(1.0, max(0.0, float(minimum)) + min(0.20, max(0.0, risk_score) * 0.20))
    if financial:
        return ConfidenceDecision(False, score, threshold, "Une action financière exige une approbation explicite.")
    if irreversible:
        return ConfidenceDecision(False, score, threshold, "Une action irréversible exige une approbation explicite.")
    if score < threshold:
        return ConfidenceDecision(False, score, threshold, "Confiance insuffisante.")
    return ConfidenceDecision(True, score, threshold, "Seuil de confiance satisfait.")

def autonomous(confidence: float, minimum: float, financial: bool = False) -> bool:
    return evaluate_confidence(confidence, minimum, financial=financial).allowed
