from integrations.shopify.client import ShopifyClient
class ScopeValidator:
    def __init__(self,client: ShopifyClient) -> None: self.client=client
    async def validate(self,required: set[str]) -> dict[str,object]:
        installation=await self.client.current_app_installation()
        granted={s["handle"] for s in installation.get("accessScopes",[])}
        missing=sorted(required-granted)
        return {"ok":not missing,"granted":sorted(granted),"missing":missing}
