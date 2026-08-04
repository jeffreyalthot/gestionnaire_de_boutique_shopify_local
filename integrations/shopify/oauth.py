from urllib.parse import urlencode
import secrets
import httpx
from config.settings import Settings

class ShopifyOAuth:
    def __init__(self, settings: Settings) -> None: self.settings=settings
    def authorization_url(self, shop: str, scopes: list[str], redirect_uri: str) -> tuple[str,str]:
        state=secrets.token_urlsafe(32)
        query=urlencode({"client_id":self.settings.shopify_client_id,"scope":",".join(scopes),
                         "redirect_uri":redirect_uri,"state":state})
        return f"https://{shop}/admin/oauth/authorize?{query}",state
    async def exchange_code(self, shop: str, code: str) -> dict[str, object]:
        async with httpx.AsyncClient(timeout=30) as client:
            response=await client.post(f"https://{shop}/admin/oauth/access_token",json={
                "client_id":self.settings.shopify_client_id,
                "client_secret":self.settings.shopify_client_secret.get_secret_value(),
                "code":code,
            })
            response.raise_for_status(); return response.json()
