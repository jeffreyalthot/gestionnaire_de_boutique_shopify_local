from tests.target_test_support import assert_alibaba_contract

def test_order_create_contract_accepts_canonical_payload():
    assert_alibaba_contract('order_create',{'supplierId': 's1', 'items': [{'sku': 'x', 'quantity': 1}], 'shippingAddress': {'country': 'CA'}})
