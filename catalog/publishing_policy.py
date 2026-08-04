from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class PublishingDecision:
    publish: bool
    score: float
    minimum_score: float
    stock: int
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_publication(score: float, eligible: bool, stock: int, minimum_score: float = 0.70) -> PublishingDecision:
    reasons: list[str] = []
    normalized = max(0.0, min(1.0, float(score)))
    if not eligible: reasons.append("product_ineligible")
    if normalized < minimum_score: reasons.append("quality_score_below_threshold")
    if int(stock) <= 0: reasons.append("stock_unavailable")
    return PublishingDecision(not reasons, normalized, float(minimum_score), int(stock), tuple(reasons))


def should_publish(score: float, eligible: bool, stock: int, minimum_score: float = 0.70) -> bool:
    return evaluate_publication(score, eligible, stock, minimum_score).publish
