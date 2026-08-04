from tests.target_test_support import assert_alibaba_contract

def test_payment_result_contract_accepts_canonical_payload():
    assert_alibaba_contract('payment_result',{'orderId': 'o1', 'status': 'paid', 'transactionId': 't1'})
