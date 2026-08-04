from tests.target_test_support import assert_alibaba_contract

def test_supplier_profile_contract_accepts_canonical_payload():
    assert_alibaba_contract('supplier_profile',{'supplierId': 's1', 'companyName': 'Supplier Inc', 'yearsActive': 5})
