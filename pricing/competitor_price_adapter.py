from decimal import Decimal
def choose_market_aware_price(calculated: Decimal,competitor_prices: list[Decimal],floor: Decimal) -> Decimal:
    valid=[Decimal(str(p)) for p in competitor_prices if Decimal(str(p))>0]
    if not valid: return max(calculated,floor)
    median=sorted(valid)[len(valid)//2]
    return max(floor,min(calculated,median))
