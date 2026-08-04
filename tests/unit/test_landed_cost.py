from decimal import Decimal
from pricing.landed_cost_calculator import LandedCostCalculator
def test_landed_cost_contains_buffers():
    x=LandedCostCalculator().calculate(Decimal("100"),Decimal("20"),Decimal("3"),Decimal("5"),Decimal("2"),Decimal("2"))
    assert x.total==Decimal("134.40")
