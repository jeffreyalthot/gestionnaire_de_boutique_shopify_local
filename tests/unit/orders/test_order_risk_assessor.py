from orders.order_risk_assessor import OrderRiskAssessor

def test_order_risk_assessor_holds_high_velocity_order():
    result=OrderRiskAssessor().assess({"amount":1200,"orders_last_hour":8,"billing_shipping_mismatch":True,"proxy_or_vpn":True})
    assert result.hold and result.level in {"high","critical"}
