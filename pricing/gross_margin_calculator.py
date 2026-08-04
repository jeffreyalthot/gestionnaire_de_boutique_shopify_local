from decimal import Decimal
def sale_price_for_margin(cost: Decimal, margin_percent: Decimal) -> Decimal:
    cost=Decimal(str(cost)); margin=Decimal(str(margin_percent))/Decimal("100")
    if margin < 0 or margin >= 1: raise ValueError("La marge doit être comprise entre 0 et moins de 100 %.")
    return cost/(Decimal("1")-margin)
def gross_margin_percent(revenue: Decimal,cost: Decimal) -> Decimal:
    revenue=Decimal(str(revenue)); cost=Decimal(str(cost))
    return Decimal("0") if revenue<=0 else (revenue-cost)/revenue*Decimal("100")
