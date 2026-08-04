from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class MarginTarget:
    target_percent: float
    floor_percent: float
    ceiling_percent: float
    adjustments: dict[str, float]
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DynamicMarginPolicy:
    def __init__(self, *, floor_percent: float = 5, ceiling_percent: float = 80) -> None:
        self.floor = float(floor_percent)
        self.ceiling = max(self.floor, float(ceiling_percent))

    def target(self, *, base_margin_percent: float, return_risk: float = 0, volatility: float = 0, competition: float = 0, shipping_risk: float = 0, supplier_risk: float = 0, conversion_pressure: float = 0) -> float:
        return self.evaluate(
            base_margin_percent=base_margin_percent,
            return_risk=return_risk,
            volatility=volatility,
            competition=competition,
            shipping_risk=shipping_risk,
            supplier_risk=supplier_risk,
            conversion_pressure=conversion_pressure,
        ).target_percent

    def evaluate(self, **signals: float) -> MarginTarget:
        base = float(signals.pop("base_margin_percent", 0))
        factors = {
            "return_risk": max(0.0, min(1.0, float(signals.get("return_risk", 0)))) * 12,
            "volatility": max(0.0, min(1.0, float(signals.get("volatility", 0)))) * 8,
            "competition": -max(0.0, min(1.0, float(signals.get("competition", 0)))) * 5,
            "shipping_risk": max(0.0, min(1.0, float(signals.get("shipping_risk", 0)))) * 7,
            "supplier_risk": max(0.0, min(1.0, float(signals.get("supplier_risk", 0)))) * 9,
            "conversion_pressure": -max(0.0, min(1.0, float(signals.get("conversion_pressure", 0)))) * 4,
        }
        raw = base + sum(factors.values())
        target = round(max(self.floor, min(self.ceiling, raw)), 2)
        positive = [key for key, value in factors.items() if value >= 2]
        negative = [key for key, value in factors.items() if value <= -2]
        reason = "base" if not positive and not negative else "risk_up:" + ",".join(positive) if positive else "market_down:" + ",".join(negative)
        return MarginTarget(target, self.floor, self.ceiling, {k: round(v, 2) for k, v in factors.items()}, reason)
