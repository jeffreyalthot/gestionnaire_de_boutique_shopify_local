from tests.target_test_support import assert_graphql_document

def test_document_is_named_and_loadable():
    text=assert_graphql_document('products/create_product.graphql')
    assert text.startswith('mutation')
