from __future__ import annotations

from dataclasses import asdict, dataclass

from orders.order_validator import OrderValidation, OrderValidator


@dataclass(frozen=True, slots=True)
class OrderQualityDecision:
    passed: bool
    score: float
    issues: tuple[str, ...]
    blocking_issues: tuple[str, ...]
    warnings: tuple[str, ...]
    action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OrderQualityGate:
    BLOCKING_PREFIXES = ("missing_order_id", "negative_total", "missing_lines", "missing_shipping_address", "invalid_line_")

    def __init__(self, validator: OrderValidator | None = None, minimum_score: float = 0.8) -> None:
        self.validator = validator or OrderValidator()
        self.minimum_score = min(1.0, max(0.0, float(minimum_score)))

    def decide(self, order: dict[str, object]) -> OrderQualityDecision:
        validation = self.validator.validate(order)
        issues = validation.issues
        blocking = tuple(issue for issue in issues if issue.startswith(self.BLOCKING_PREFIXES))
        warnings = tuple(issue for issue in issues if issue not in blocking)
        denominator = max(5, 5 + len(issues))
        score = max(0.0, 1.0 - (len(blocking) * 0.25 + len(warnings) * 0.08))
        passed = not blocking and score >= self.minimum_score
        action = "accept" if passed else "hold_for_review" if not blocking else "reject_or_correct"
        return OrderQualityDecision(passed, round(score, 4), issues, blocking, warnings, action)

    def evaluate(self, order: dict[str, object]) -> OrderValidation:
        return self.validator.validate(order)
