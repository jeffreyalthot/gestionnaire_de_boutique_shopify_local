from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DueDiligenceResult:
    accepted: bool
    reasons: tuple[str, ...]


class DueDiligence:
    def evaluate(self, profile: dict[str, object]) -> DueDiligenceResult:
        reasons: list[str] = []
        if not profile.get("verified_business"):
            reasons.append("business_not_verified")
        if float(profile.get("years_active", 0) or 0) < 1:
            reasons.append("insufficient_history")
        if float(profile.get("dispute_rate", 1) or 1) > 0.05:
            reasons.append("high_dispute_rate")
        if not profile.get("trade_assurance"):
            reasons.append("trade_assurance_missing")
        if profile.get("sanctions_match"):
            reasons.append("sanctions_match")
        return DueDiligenceResult(not reasons, tuple(reasons))
