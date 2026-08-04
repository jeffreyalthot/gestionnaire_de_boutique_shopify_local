from __future__ import annotations
from domain.value_objects.idempotency_key import build_idempotency_key
from infrastructure.queue.durable_queue import DurableQueue
from integrations.shopify.webhooks.envelope import ShopifyWebhookEnvelope
class ShopifyWebhookDispatcher:
    def __init__(self, queue: DurableQueue) -> None:
        self.queue = queue
    def dispatch(self, webhook_id: str, topic: str, shop: str, payload: dict[str, object], *, event_id: str = "", api_version: str = "", triggered_at: str = "") -> str:
        envelope = ShopifyWebhookEnvelope.create(webhook_id=webhook_id, event_id=event_id, topic=topic, shop_domain=shop, api_version=api_version, triggered_at=triggered_at, payload=payload)
        return self.queue.enqueue("shopify_webhook", envelope.to_dict(), build_idempotency_key("shopify-webhook", webhook_id), queue="shopify", priority=20)
