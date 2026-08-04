from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from finance.money_math import decimal_money
@dataclass(frozen=True, slots=True)
class CurrencyVariance:
    expected_cad: Decimal
    actual_cad: Decimal
    gain_loss_cad: Decimal
    favorable: bool

def calculate_currency_gain_loss(expected_cad: object, actual_cad: object) -> CurrencyVariance:
    expected, actual = decimal_money(expected_cad), decimal_money(actual_cad)
    delta = expected - actual
    return CurrencyVariance(expected, actual, delta, delta >= 0)
def currency_gain_loss(expected_cad: float, actual_cad: float) -> float:
    return float(calculate_currency_gain_loss(expected_cad, actual_cad).gain_loss_cad)
