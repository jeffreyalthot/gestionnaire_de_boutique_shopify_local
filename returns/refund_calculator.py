from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefundBreakdown:
    subtotal: float
    tax: float
    shipping: float
    restocking_fee: float
    total: float


class RefundCalculator:
    def calculate(self, subtotal: float, tax: float, shipping: float, *, refund_shipping: bool, restocking_percent: float = 0.0) -> RefundBreakdown:
        fee = max(0.0, subtotal * restocking_percent / 100)
        total = max(0.0, subtotal + tax + (shipping if refund_shipping else 0.0) - fee)
        return RefundBreakdown(round(subtotal, 2), round(tax, 2), round(shipping if refund_shipping else 0.0, 2), round(fee, 2), round(total, 2))
