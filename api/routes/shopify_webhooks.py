from __future__ import annotations

from fastapi import APIRouter

from integrations.shopify.webhooks.receiver import build_shopify_webhook_router

__all__ = ["build_shopify_webhook_router", "router_from_container"]


def router_from_container(container) -> APIRouter:
    """Build the Shopify router from canonical container dependencies."""
    from integrations.shopify.webhooks.deduplicator import WebhookDeduplicator
    from integrations.shopify.webhooks.dispatcher import ShopifyWebhookDispatcher

    deduplicator = WebhookDeduplicator(container.db)
    dispatcher = ShopifyWebhookDispatcher(container.queue)
    return build_shopify_webhook_router(container.settings, deduplicator, dispatcher)
