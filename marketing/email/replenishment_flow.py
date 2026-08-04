from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReplenishmentDecision:
    due: bool
    days_remaining: int
    reason: str
class ReplenishmentFlow:
    def evaluate(self, days_since_purchase: int, expected_lifetime_days: int, *, marketing_consent: bool = True, already_contacted: bool = False) -> ReplenishmentDecision:
        if not marketing_consent:
            return ReplenishmentDecision(False, 0, "Consentement marketing absent.")
        if already_contacted:
            return ReplenishmentDecision(False, 0, "Client déjà contacté pour ce cycle.")
        if expected_lifetime_days <= 0:
            return ReplenishmentDecision(False, 0, "Durée de vie produit inconnue.")
        trigger = max(1, round(expected_lifetime_days * 0.85))
        remaining = max(0, trigger - max(0, days_since_purchase))
        return ReplenishmentDecision(remaining == 0, remaining, "Réapprovisionnement probablement requis." if remaining == 0 else "Fenêtre de réapprovisionnement non atteinte.")
    def due(self, days_since_purchase: int, expected_lifetime_days: int) -> bool:
        return self.evaluate(days_since_purchase, expected_lifetime_days).due
