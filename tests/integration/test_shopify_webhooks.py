from integrations.shopify.webhooks.deduplicator import WebhookDeduplicator
def test_dedup(db):
    d=WebhookDeduplicator(db); assert d.register("id","orders/paid","shop",{"id":1}); assert not d.register("id","orders/paid","shop",{"id":1})
