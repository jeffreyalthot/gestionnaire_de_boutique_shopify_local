from integrations.alibaba.client import AlibabaClient
from integrations.alibaba.mappers.shipping_mapper import map_shipping_quote
from fulfillment.shipping_quote_cache import ShippingQuoteCache
class ShippingQuoteEngine:
    def __init__(self,client: AlibabaClient,cache: ShippingQuoteCache|None=None) -> None:
        self.client=client; self.cache=cache or ShippingQuoteCache()
    async def quote(self,product_id: str,sku_id: str,quantity: int,country: str,postal: str) -> dict[str,object]:
        key=self.cache.key(product_id,sku_id,country,postal,quantity)
        cached=self.cache.get(key)
        if cached: return cached
        result=map_shipping_quote(await self.client.calculate_product_freight(product_id,sku_id,quantity,country,postal))
        self.cache.set(key,result,1800)
        return result
