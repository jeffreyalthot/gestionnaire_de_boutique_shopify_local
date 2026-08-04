from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class LandedCostBreakdown:
    product_cost: Decimal
    shipping_cost: Decimal
    service_fees: Decimal
    duties_taxes: Decimal
    currency_buffer: Decimal
    refund_reserve: Decimal
    total: Decimal

class LandedCostCalculator:
    def calculate(self, product_cost: Decimal, shipping_cost: Decimal, platform_fee_percent: Decimal,
                  duty_tax_percent: Decimal, currency_buffer_percent: Decimal,
                  refund_reserve_percent: Decimal) -> LandedCostBreakdown:
        product_cost=Decimal(str(product_cost)); shipping_cost=Decimal(str(shipping_cost))
        base=product_cost+shipping_cost
        fees=base*Decimal(str(platform_fee_percent))/Decimal("100")
        duties=base*Decimal(str(duty_tax_percent))/Decimal("100")
        currency=base*Decimal(str(currency_buffer_percent))/Decimal("100")
        reserve=base*Decimal(str(refund_reserve_percent))/Decimal("100")
        total=base+fees+duties+currency+reserve
        return LandedCostBreakdown(product_cost,shipping_cost,fees,duties,currency,reserve,total)
