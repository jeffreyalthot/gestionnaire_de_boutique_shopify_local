from __future__ import annotations
from fastapi import APIRouter, Header, HTTPException, Request, Response
from config.settings import Settings
from integrations.shopify.webhooks.deduplicator import WebhookDeduplicator
from integrations.shopify.webhooks.dispatcher import ShopifyWebhookDispatcher
from security.webhook_security import verify_shopify_hmac

def build_shopify_webhook_router(settings: Settings, deduplicator: WebhookDeduplicator, dispatcher: ShopifyWebhookDispatcher) -> APIRouter:
    router = APIRouter()
    @router.post("/webhooks/shopify")
    async def receive(
        request: Request,
        x_shopify_hmac_sha256: str = Header(default=""),
        x_shopify_webhook_id: str = Header(default=""),
        x_shopify_event_id: str = Header(default=""),
        x_shopify_topic: str = Header(default=""),
        x_shopify_shop_domain: str = Header(default=""),
        x_shopify_api_version: str = Header(default=""),
        x_shopify_triggered_at: str = Header(default=""),
    ) -> Response:
        body = await request.body()
        if len(body) > settings.shopify_webhook_max_body_bytes:
            raise HTTPException(status_code=413, detail="Webhook Shopify trop volumineux.")
        if not verify_shopify_hmac(body, x_shopify_hmac_sha256, settings.shopify_webhook_secret.get_secret_value(), max_body_bytes=settings.shopify_webhook_max_body_bytes):
            raise HTTPException(status_code=401, detail="Signature Shopify invalide.")
        if not x_shopify_webhook_id or not x_shopify_topic or not x_shopify_shop_domain:
            raise HTTPException(status_code=400, detail="En-têtes webhook incomplets.")
        try:
            payload = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="JSON invalide.") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Le payload webhook doit être un objet JSON.")
        inserted = deduplicator.register(x_shopify_webhook_id, x_shopify_topic, x_shopify_shop_domain, payload)
        if inserted:
            dispatcher.dispatch(x_shopify_webhook_id, x_shopify_topic, x_shopify_shop_domain, payload, event_id=x_shopify_event_id, api_version=x_shopify_api_version, triggered_at=x_shopify_triggered_at)
        return Response(status_code=200, headers={"X-Orchestrator-Deduplicated": "0" if inserted else "1"})
    return router
