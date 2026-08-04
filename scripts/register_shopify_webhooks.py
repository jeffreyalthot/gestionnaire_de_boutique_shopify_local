import asyncio,json
from app.bootstrap import bootstrap
from integrations.shopify.webhooks.subscription_manager import WebhookSubscriptionManager
TOPICS=["orders/create","orders/updated","orders/paid","orders/cancelled","orders/fulfilled","refunds/create",
"products/update","products/delete","inventory_levels/update","fulfillments/update","app/uninstalled","app/scopes_update"]
async def run():
    app=bootstrap()
    try:
        if not app.settings.live_shopify_ready: raise RuntimeError("Shopify non configuré.")
        base=app.settings.shopify_callback_base_url or app.settings.app_public_base_url
        return await WebhookSubscriptionManager(app.container.shopify).ensure(base,TOPICS)
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2,default=str))
