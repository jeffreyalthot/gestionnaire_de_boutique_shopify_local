from integrations.shopify.webhooks.handler_registry import ShopifyWebhookHandlerRegistry
from integrations.shopify.webhooks.handlers.orders_paid import handle

def test_handler_result_contains_fingerprint_and_followups():
    result=handle({"id":123,"updated_at":"2026-01-01T00:00:00Z","status":"paid"})
    assert result["entity_id"]=="123" and len(result["fingerprint"])==64
    assert "supplier_order_planning" in result["follow_up_operations"]
def test_registry_loads_all_default_handlers():
    registry=ShopifyWebhookHandlerRegistry();count=registry.load_defaults()
    assert count>=30 and "orders/paid" in registry.topics()
    assert registry.handle("unknown/topic",{})["action"]=="unhandled"
