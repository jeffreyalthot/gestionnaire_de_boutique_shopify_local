from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EscalationDecision:
    escalate: bool
    team: str
    priority: int
    reason: str


class EscalationPolicy:
    TEAMS = {"chargeback": "finance", "fraud": "risk", "privacy": "compliance", "legal": "compliance",
             "lost_package": "fulfillment", "damaged_item": "returns", "refund": "returns", "cancellation": "orders"}

    def decide(self, *, category: str, sla_breached: bool = False, amount_cad: float = 0.0,
               repeated_contacts: int = 0, customer_risk: float = 0.0) -> EscalationDecision:
        team = self.TEAMS.get(category, "customer_service")
        reasons: list[str] = []
        priority = 100
        if category in {"chargeback", "fraud", "legal", "privacy"}:
            reasons.append("sensitive_category"); priority = min(priority, 10)
        if sla_breached:
            reasons.append("sla_breached"); priority = min(priority, 20)
        if amount_cad >= 250:
            reasons.append("high_value"); priority = min(priority, 25)
        if repeated_contacts >= 3:
            reasons.append("repeat_contact"); priority = min(priority, 30)
        if customer_risk >= 0.75:
            reasons.append("high_risk"); priority = min(priority, 15)
        return EscalationDecision(bool(reasons), team, priority, ",".join(reasons) or "routine")
