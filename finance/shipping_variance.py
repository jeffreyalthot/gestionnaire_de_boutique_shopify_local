from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from finance.money_math import decimal_money
@dataclass(frozen=True, slots=True)
class ShippingVariance:
    charged: Decimal
    actual: Decimal
    variance: Decimal
    recovered_cost: bool

def calculate_shipping_variance(charged: object, actual: object) -> ShippingVariance:
    charged_amount, actual_amount = decimal_money(charged), decimal_money(actual)
    variance = charged_amount - actual_amount
    return ShippingVariance(charged_amount, actual_amount, variance, variance >= 0)
def shipping_variance(charged: float, actual: float) -> float:
    return float(calculate_shipping_variance(charged, actual).variance)
