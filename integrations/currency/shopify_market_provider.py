from decimal import Decimal
from integrations.shopify.client import ShopifyClient
class ShopifyMarketRateProvider:
    def __init__(self,client: ShopifyClient,fallback) -> None: self.client=client; self.fallback=fallback
    async def rate(self,source: str,target: str) -> Decimal: return await self.fallback.rate(source,target)
