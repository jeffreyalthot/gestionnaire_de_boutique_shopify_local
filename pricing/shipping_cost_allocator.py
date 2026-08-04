from decimal import Decimal
def allocate_shipping(total_shipping: Decimal,quantities: list[int]) -> list[Decimal]:
    total_units=sum(quantities)
    if total_units<=0: return [Decimal("0") for _ in quantities]
    return [Decimal(str(total_shipping))*Decimal(q)/Decimal(total_units) for q in quantities]
