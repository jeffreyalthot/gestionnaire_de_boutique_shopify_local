from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class PriceGuardrailDecision:
    allowed: bool
    price: Decimal
    cost: Decimal
    profit: Decimal
    margin_percent: Decimal
    markup_percent: Decimal
    violations: tuple[str, ...]
    warnings: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key in ("price", "cost", "profit", "margin_percent", "markup_percent"):
            data[key] = str(data[key])
        return data


class PriceGuardrails:
    def evaluate(
        self,
        price: object,
        cost: object,
        minimum_margin_percent: object,
        *,
        maximum_multiplier: object = 10,
        minimum_profit_cad: object = 0,
        reference_price: object | None = None,
        maximum_change_percent: object = 50,
    ) -> PriceGuardrailDecision:
        p = Decimal(str(price)); c = Decimal(str(cost))
        violations: list[str] = []
        warnings: list[str] = []
        if p <= 0 or c < 0:
            violations.append("invalid_price_or_cost")
        profit = p - c
        margin = (profit / p * 100) if p > 0 else Decimal("0")
        markup = (profit / c * 100) if c > 0 else Decimal("0")
        if c and p > c * Decimal(str(maximum_multiplier)):
            violations.append("maximum_multiplier_exceeded")
        if margin < Decimal(str(minimum_margin_percent)):
            violations.append("minimum_margin_not_met")
        if profit < Decimal(str(minimum_profit_cad)):
            violations.append("minimum_profit_not_met")
        if reference_price is not None:
            ref = Decimal(str(reference_price))
            change = abs(p - ref) / ref * 100 if ref > 0 else Decimal("0")
            if change > Decimal(str(maximum_change_percent)):
                warnings.append("large_price_change")
        return PriceGuardrailDecision(
            not violations,
            p.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            c.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            profit.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            margin.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            markup.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            tuple(violations),
            tuple(warnings),
        )


def validate_price(price: Decimal, cost: Decimal, minimum_margin_percent: Decimal, maximum_multiplier: Decimal = Decimal("10")) -> None:
    decision = PriceGuardrails().evaluate(price, cost, minimum_margin_percent, maximum_multiplier=maximum_multiplier)
    if decision.violations:
        messages = {
            "invalid_price_or_cost": "Prix ou coût invalide.",
            "maximum_multiplier_exceeded": "Prix au-delà de la limite de sécurité.",
            "minimum_margin_not_met": "Marge sous le minimum configuré.",
            "minimum_profit_not_met": "Profit sous le minimum configuré.",
        }
        raise ValueError(messages[decision.violations[0]])
