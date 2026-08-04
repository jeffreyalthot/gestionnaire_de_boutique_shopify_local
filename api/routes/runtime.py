from fastapi import APIRouter
from app.liveness import liveness
from app.readiness import readiness

def router_for(container):
    router=APIRouter(prefix="/runtime",tags=["runtime"])
    @router.get("/liveness")
    async def live():return liveness()
    @router.get("/readiness")
    async def ready():return await readiness(container)
    @router.get("/services")
    async def services():return container.service_registry.snapshot()
    @router.get("/integrations")
    async def integrations():return {"webhooks":container.webhook_handlers.snapshot(),"sales_channels":container.sales_channels.snapshot(),"capabilities":container.capabilities.snapshot()}
    return router
