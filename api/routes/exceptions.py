from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.operator_auth import OperatorAuthorizer


def router_for(container):
    router = APIRouter(prefix="/exceptions", tags=["exceptions"])
    authorizer = OperatorAuthorizer(container.settings)

    @router.get("")
    async def list_exceptions(limit: int = Query(50, ge=1, le=500)):
        return {"items": container.exception_queue.claim_ready(limit), "stats": container.exception_queue.stats()}

    @router.post("/{exception_id}/resolve", dependencies=[Depends(authorizer.require)])
    async def resolve(exception_id: str, status: str = "resolved"):
        container.exception_queue.resolve(exception_id, status)
        return {"id": exception_id, "status": status}

    return router
