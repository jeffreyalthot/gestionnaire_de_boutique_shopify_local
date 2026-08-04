from __future__ import annotations

from dataclasses import dataclass

from orders.order_deduplicator import OrderDeduplicator
from orders.order_normalizer import OrderNormalizer
from orders.order_validator import OrderValidator


@dataclass(frozen=True, slots=True)
class IntakeResult:
    accepted: bool
    order: dict[str, object]
    fingerprint: str
    issues: tuple[str, ...] = ()


class OrderIntake:
    def __init__(self) -> None:
        self.normalizer=OrderNormalizer(); self.validator=OrderValidator(); self.deduplicator=OrderDeduplicator()

    def process(self, raw: dict[str, object], known_fingerprints: set[str] | None = None) -> IntakeResult:
        order=self.normalizer.normalize(raw); fp=self.deduplicator.fingerprint(order)
        if fp in (known_fingerprints or set()):
            return IntakeResult(False, order, fp, ("duplicate",))
        result=self.validator.validate(order)
        return IntakeResult(result.valid, order, fp, result.issues)
