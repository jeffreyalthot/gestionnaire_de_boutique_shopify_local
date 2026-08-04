from decimal import Decimal
from domain.value_objects.money import Money
def test_money_arithmetic():
    assert (Money(Decimal("1.005"))+Money(Decimal("2"))).amount==Decimal("3.01")
