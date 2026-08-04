from tests.target_test_support import assert_graphql_document

def test_document_is_named_and_loadable():
    text=assert_graphql_document('products/query_products.graphql')
    assert text.startswith('query')
