from __future__ import annotations
import json
from integrations.shopify.webhooks.hmac_verifier import verify_shopify_hmac
class ShopifyEventsReceiver:
    def __init__(self,secret: str,dispatcher)->None:self.secret=secret;self.dispatcher=dispatcher
    def receive(self,headers: dict[str,str],body: bytes)->str:
        signature=headers.get('X-Shopify-Hmac-Sha256','')
        if not verify_shopify_hmac(self.secret,body,signature):raise PermissionError('HMAC Shopify invalide.')
        topic=headers.get('X-Shopify-Topic','');webhook_id=headers.get('X-Shopify-Webhook-Id','');shop=headers.get('X-Shopify-Shop-Domain','')
        if not topic or not webhook_id or not shop:raise ValueError('En-têtes Shopify incomplets.')
        return self.dispatcher.dispatch(webhook_id,topic,shop,json.loads(body))
