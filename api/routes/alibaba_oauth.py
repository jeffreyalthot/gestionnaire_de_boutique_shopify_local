from fastapi import APIRouter
def router_for(oauth):
    router=APIRouter()
    @router.get("/oauth/alibaba/start")
    async def start(): url,state=oauth.authorization_url(); return {"url":url,"state":state}
    return router
