from inventory.safety_stock import available_for_sale
def test_safety_stock(): assert available_for_sale(10,2,3)==5
