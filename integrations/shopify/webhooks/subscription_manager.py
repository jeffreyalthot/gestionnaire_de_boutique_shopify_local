from integrations.shopify.client import ShopifyClient
TOPIC_MAP={
"orders/create":"ORDERS_CREATE","orders/updated":"ORDERS_UPDATED","orders/paid":"ORDERS_PAID",
"orders/cancelled":"ORDERS_CANCELLED","orders/fulfilled":"ORDERS_FULFILLED","refunds/create":"REFUNDS_CREATE",
"products/update":"PRODUCTS_UPDATE","products/delete":"PRODUCTS_DELETE",
"inventory_levels/update":"INVENTORY_LEVELS_UPDATE","fulfillments/update":"FULFILLMENTS_UPDATE",
"app/uninstalled":"APP_UNINSTALLED","app/scopes_update":"APP_SCOPES_UPDATE",
}
class WebhookSubscriptionManager:
    def __init__(self,client: ShopifyClient) -> None: self.client=client
    async def ensure(self,base_url: str,topics: list[str]) -> list[dict[str,object]]:
        existing=await self.client.webhooks(); existing_topics={x["topic"] for x in existing}
        created=[]
        for topic in topics:
            gql_topic=TOPIC_MAP.get(topic,topic.upper().replace("/","_"))
            if gql_topic not in existing_topics:
                created.append(await self.client.create_webhook(gql_topic,base_url.rstrip("/")+"/webhooks/shopify"))
        return created
