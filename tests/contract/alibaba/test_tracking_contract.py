from tests.target_test_support import assert_alibaba_contract

def test_tracking_contract_accepts_canonical_payload():
    assert_alibaba_contract('tracking',{'orderId': 'o1', 'trackingNumber': 'T1', 'status': 'in_transit', 'events': []})
