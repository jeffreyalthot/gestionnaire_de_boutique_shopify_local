import httpx
from config.settings import Settings
class ShopifyRestCompatibilityClient:
    def __init__(self,settings: Settings) -> None: self.settings=settings
    async def get(self,path: str) -> dict[str,object]:
        if not self.settings.shopify_enable_rest_compatibility:
            raise RuntimeError("Adaptateur REST désactivé.")
        url=f"https://{self.settings.shopify_shop_domain}/admin/api/{self.settings.shopify_api_version}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.settings.shopify_request_timeout_seconds) as client:
            response=await client.get(url,headers={"X-Shopify-Access-Token":self.settings.shopify_admin_access_token.get_secret_value()})
            response.raise_for_status(); return response.json()
