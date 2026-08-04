from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class WinbackDecision:
    eligible: bool
    segment: str
    reason: str
class WinbackFlow:
    def evaluate(self, days_since_order: int, marketing_consent: bool, *, lifetime_orders: int = 1, complaint_open: bool = False, minimum_days: int = 120) -> WinbackDecision:
        if not marketing_consent:
            return WinbackDecision(False, "excluded", "Consentement marketing absent.")
        if complaint_open:
            return WinbackDecision(False, "service_recovery", "Un dossier de service est ouvert.")
        if days_since_order < minimum_days:
            return WinbackDecision(False, "active", "Client encore actif.")
        segment = "vip_lapsed" if lifetime_orders >= 5 else "lapsed"
        return WinbackDecision(True, segment, "Client admissible à une campagne de reconquête.")
    def eligible(self, days_since_order: int, marketing_consent: bool) -> bool:
        return self.evaluate(days_since_order, marketing_consent).eligible
