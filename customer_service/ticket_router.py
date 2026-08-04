from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class TicketRoute:
    team: str
    priority: str
    sla_minutes: int
    automation_allowed: bool
    reason: str
    tags: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class TicketRouter:
    ROUTES = {
        "chargeback": "finance",
        "fraud": "risk",
        "lost_package": "fulfillment",
        "damaged_item": "returns",
        "refund": "returns",
        "cancellation": "orders",
        "shipping": "fulfillment",
        "privacy": "compliance",
        "product_safety": "compliance",
        "supplier": "procurement",
    }
    PRIORITY = {"chargeback": "critical", "fraud": "critical", "product_safety": "critical", "lost_package": "high", "damaged_item": "high", "refund": "medium"}
    SLA = {"critical": 15, "high": 60, "medium": 240, "normal": 720}

    def route(self, category: str) -> str:
        return self.plan(category).team

    def plan(self, category: str, *, customer_tier: str = "standard", amount_cad: float = 0, sentiment: float = 0) -> TicketRoute:
        key = str(category).strip().lower().replace(" ", "_")
        team = self.ROUTES.get(key, "customer_service")
        priority = self.PRIORITY.get(key, "normal")
        if customer_tier.lower() in {"vip", "high_value"} and priority == "normal":
            priority = "medium"
        if amount_cad >= 500 and priority in {"normal", "medium"}:
            priority = "high"
        if sentiment <= -0.7 and priority == "normal":
            priority = "medium"
        automation = priority not in {"critical"} and key not in {"fraud", "chargeback", "product_safety", "privacy"}
        return TicketRoute(team, priority, self.SLA[priority], automation, key or "uncategorized", tuple(filter(None, (key, customer_tier))))
