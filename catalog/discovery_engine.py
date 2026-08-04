from integrations.alibaba.client import AlibabaClient
class ProductDiscoveryEngine:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    async def discover(self,keywords: list[str],page_size: int=20) -> list[dict[str,object]]:
        found=[]
        for keyword in keywords:
            payload=await self.client.search_distribution_products(keyword,page_size=page_size)
            items=payload.get("products") or payload.get("result") or payload.get("items") or []
            if isinstance(items,list): found.extend(x for x in items if isinstance(x,dict))
        return found
