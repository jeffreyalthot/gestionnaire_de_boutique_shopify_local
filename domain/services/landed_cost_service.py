from __future__ import annotations

from decimal import Decimal

from pricing.landed_cost_calculator import LandedCostBreakdown, LandedCostCalculator

__all__ = ["LandedCostCalculator", "LandedCostBreakdown", "calculate_landed_cost"]


def calculate_landed_cost(
    product_cost: Decimal,
    shipping_cost: Decimal,
    *,
    platform_fee_percent: Decimal = Decimal("0"),
    duty_percent: Decimal = Decimal("0"),
    currency_buffer_percent: Decimal = Decimal("0"),
    refund_reserve_percent: Decimal = Decimal("0"),
) -> LandedCostBreakdown:
    return LandedCostCalculator().calculate(
        Decimal(str(product_cost)), Decimal(str(shipping_cost)),
        Decimal(str(platform_fee_percent)), Decimal(str(duty_percent)),
        Decimal(str(currency_buffer_percent)), Decimal(str(refund_reserve_percent)),
    )
