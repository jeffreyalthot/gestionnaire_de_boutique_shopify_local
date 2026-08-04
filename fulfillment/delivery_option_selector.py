from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True, slots=True)
class DeliverySelection:
    option: dict[str, object]
    score: float
    eligible_count: int
    rejected_count: int
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["option"] = dict(self.option)
        return result


def _number(value: object, default: float) -> float:
    try:
        return float(Decimal(str(value)))
    except (InvalidOperation, ValueError, TypeError):
        return default


class DeliveryOptionSelector:
    def select(
        self,
        options: list[dict[str, object]],
        *,
        maximum_days: int = 60,
        maximum_amount_cad: float | None = None,
        tracking_required: bool = True,
        preferred_carriers: tuple[str, ...] = (),
        cost_weight: float = 0.55,
        speed_weight: float = 0.35,
        reliability_weight: float = 0.10,
    ) -> DeliverySelection:
        eligible: list[tuple[float, dict[str, object], tuple[str, ...]]] = []
        rejected = 0
        carriers = {item.casefold() for item in preferred_carriers}
        for raw in options:
            option = dict(raw)
            days = max(0, int(_number(option.get("estimated_days"), 999)))
            amount = max(0.0, _number(option.get("amount", option.get("amount_cad")), float("inf")))
            tracked = bool(option.get("tracking", option.get("trackable", True)))
            if days > max(1, int(maximum_days)) or (maximum_amount_cad is not None and amount > maximum_amount_cad) or (tracking_required and not tracked):
                rejected += 1
                continue
            reliability = min(1.0, max(0.0, _number(option.get("reliability", 0.75), 0.75)))
            carrier = str(option.get("carrier", "")).casefold()
            preference_bonus = 0.08 if carrier and carrier in carriers else 0.0
            normalized_cost = amount / max(1.0, maximum_amount_cad or max(amount, 1.0))
            normalized_speed = days / max(1.0, float(maximum_days))
            score = (
                cost_weight * normalized_cost
                + speed_weight * normalized_speed
                + reliability_weight * (1.0 - reliability)
                - preference_bonus
            )
            eligible.append((score, option, ("preferred_carrier",) if preference_bonus else ()))
        if not eligible:
            raise ValueError("Aucune option de livraison admissible.")
        score, option, reasons = min(eligible, key=lambda item: (item[0], _number(item[1].get("amount"), 0), int(_number(item[1].get("estimated_days"), 999))))
        return DeliverySelection(option, round(score, 6), len(eligible), rejected, reasons)


def select_option(options: list[dict[str, object]], maximum_days: int = 60) -> dict[str, object]:
    return DeliveryOptionSelector().select(options, maximum_days=maximum_days).option
