from fastapi import APIRouter
def router_for(container):
    router=APIRouter()
    @router.get("/dashboard")
    async def dashboard(): return container.dashboard_state()
    return router
