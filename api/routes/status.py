from fastapi import APIRouter
def router_for(container):
    router=APIRouter()
    @router.get("/status")
    async def status(): return container.status()
    return router
