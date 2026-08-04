from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
def psychological_price(value: Decimal,ending: Decimal=Decimal("0.99")) -> Decimal:
    value=Decimal(str(value)); ending=Decimal(str(ending))
    whole=value.to_integral_value(rounding=ROUND_CEILING)
    candidate=whole-Decimal("1")+ending
    if candidate<value: candidate=whole+ending
    return candidate.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
