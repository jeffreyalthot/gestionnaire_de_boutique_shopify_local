from integrations.shopify.client import ShopifyClient
class ShopifyBulkOperations:
    def __init__(self,client: ShopifyClient) -> None: self.client=client
    async def export_products(self) -> dict[str,object]:
        return await self.client.bulk_query("""{products{edges{node{id title status variants{edges{node{id sku price inventoryQuantity}}}}}}}""")
