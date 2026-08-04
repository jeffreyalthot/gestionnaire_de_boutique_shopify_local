from fastapi import APIRouter
def router_for(oauth):
    router=APIRouter()
    @router.get("/oauth/shopify/start")
    async def start(shop: str,redirect_uri: str,scopes: str):
        url,state=oauth.authorization_url(shop,scopes.split(","),redirect_uri); return {"url":url,"state":state}
    return router
