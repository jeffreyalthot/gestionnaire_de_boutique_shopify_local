from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AutonomyDecision:
    allowed: bool
    simulated: bool
    approval_required: bool
    reason: str
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutonomyController:
    """Décide si une action peut être simulée, exécutée ou doit être approuvée."""

    MUTATING_RISKS = {"write", "external_write", "financial", "destructive"}

    def __init__(self, *, dry_run: bool, minimum_confidence: float = 0.92, financial_limit_cad: float = 1000.0) -> None:
        self.dry_run = dry_run
        self.minimum_confidence = max(0.0, min(1.0, minimum_confidence))
        self.financial_limit_cad = max(0.0, financial_limit_cad)

    def decide(self, *, risk: str, confidence: float = 1.0, amount_cad: float = 0.0,
               approved: bool = False, capability_available: bool = True) -> AutonomyDecision:
        confidence = max(0.0, min(1.0, float(confidence)))
        if not capability_available:
            return AutonomyDecision(False, self.dry_run, False, "capability_unavailable", confidence)
        if confidence < self.minimum_confidence:
            return AutonomyDecision(False, self.dry_run, True, "confidence_below_threshold", confidence)
        if self.dry_run:
            return AutonomyDecision(True, True, False, "dry_run", confidence)
        if risk == "financial":
            if amount_cad > self.financial_limit_cad:
                return AutonomyDecision(False, False, True, "financial_limit_exceeded", confidence)
            if not approved:
                return AutonomyDecision(False, False, True, "approval_required", confidence)
        elif risk in {"destructive", "external_write"} and not approved:
            return AutonomyDecision(False, False, True, "approval_required", confidence)
        return AutonomyDecision(True, False, False, "allowed", confidence)
