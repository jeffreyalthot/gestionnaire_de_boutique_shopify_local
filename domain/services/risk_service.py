from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    level: str
    score: float
    reasons: tuple[str, ...]
    hold: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def risk_level(order_total: float, address_complete: bool, shopify_risk: str = "") -> str:
    return assess_risk(order_total, address_complete, shopify_risk).level


def assess_risk(
    order_total: float,
    address_complete: bool,
    shopify_risk: str = "",
    *,
    velocity_count: int = 0,
    billing_shipping_mismatch: bool = False,
) -> RiskAssessment:
    score = 0.0
    reasons: list[str] = []
    if not address_complete:
        score += 0.55; reasons.append("incomplete_address")
    risk = str(shopify_risk).lower()
    if risk in {"high", "critical"}:
        score += 0.65; reasons.append("shopify_high_risk")
    elif risk == "medium":
        score += 0.30; reasons.append("shopify_medium_risk")
    if float(order_total) >= 1000:
        score += 0.25; reasons.append("high_value")
    if velocity_count >= 5:
        score += min(0.35, velocity_count * 0.04); reasons.append("high_velocity")
    if billing_shipping_mismatch:
        score += 0.20; reasons.append("address_mismatch")
    score = min(1.0, score)
    level = "high" if score >= 0.65 else ("medium" if score >= 0.30 else "low")
    return RiskAssessment(level, round(score, 4), tuple(reasons), level == "high")
