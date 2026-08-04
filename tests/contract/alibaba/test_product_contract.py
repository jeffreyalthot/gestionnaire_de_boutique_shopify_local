from tests.target_test_support import assert_alibaba_contract

def test_product_detail_contract_accepts_canonical_payload():
    assert_alibaba_contract('product_detail',{'productId': 'p1', 'title': 'Produit', 'supplierId': 's1', 'images': []})
