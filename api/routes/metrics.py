from fastapi import APIRouter
from observability.metrics import metrics
def router_for():
    router=APIRouter()
    @router.get("/metrics")
    async def get_metrics(): return metrics.snapshot()
    return router
