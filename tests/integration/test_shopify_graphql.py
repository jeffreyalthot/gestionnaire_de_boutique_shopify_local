def test_shopify_url(settings):
    configured=settings.model_copy(update={"shopify_shop_domain":"demo.myshopify.com"})
    assert configured.shopify_graphql_url.endswith("/admin/api/2026-07/graphql.json")
