from __future__ import annotations

from fastapi import APIRouter, Response, status


def router_for(container):
    router = APIRouter(tags=["health"])

    @router.get("/health")
    async def health(response: Response):
        report = await container.health.collect()
        if report["status"] == "unhealthy":
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return report

    @router.get("/ready")
    async def ready(response: Response):
        report = await container.health.collect()
        ready = bool(report["ok"])
        if not ready:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"ready": ready, "status": report["status"], "failures": report["critical_failures"]}

    @router.get("/live")
    async def live():
        return {"live": True}

    return router
