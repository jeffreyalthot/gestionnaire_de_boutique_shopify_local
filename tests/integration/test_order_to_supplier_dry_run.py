from orders.order_router import route_order
from orders.supplier_line_mapper import SupplierLineMapper

def test_paid_low_risk_order_routes_to_supplier_group():
    assert route_order({"financial_status":"paid","risk_level":"low"})=="procurement"
    groups=SupplierLineMapper().group([{"supplier_id":"s1","supplier_product_id":"p1","quantity":2}])
    assert groups["s1"][0]["quantity"]==2
