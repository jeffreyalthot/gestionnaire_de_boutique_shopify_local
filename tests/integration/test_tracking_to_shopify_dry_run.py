from tests.target_test_support import assert_graphql_document

def test_tracking_update_contract_is_available():
    text=assert_graphql_document("fulfillment/update_tracking.graphql")
    assert "tracking" in text.lower()
