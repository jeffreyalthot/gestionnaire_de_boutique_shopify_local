from orders.order_router import route_order

def test_order_router_covers_payment_risk_and_procurement():
    assert route_order({"financial_status":"pending"})=="await_payment"
    assert route_order({"financial_status":"paid","risk_level":"critical"})=="manual_risk_review"
    assert route_order({"financial_status":"paid","risk_level":"low"})=="procurement"
