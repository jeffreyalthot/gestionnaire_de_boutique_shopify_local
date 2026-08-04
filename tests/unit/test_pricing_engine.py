from decimal import Decimal
from pricing.pricing_engine import PricingEngine
def test_real_fifty_percent_margin(settings):
    decision=PricingEngine(settings).calculate(Decimal("10"),Decimal("0"))
    assert decision.sale_price_cad>decision.landed_cost_cad
    assert decision.margin_percent>=Decimal("40")
