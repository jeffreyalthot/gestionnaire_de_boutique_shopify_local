from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Query

from api.operator_auth import OperatorAuthorizer


def router_for(container):
    router = APIRouter(prefix="/automation", tags=["automation"])
    authorizer = OperatorAuthorizer(container.settings)

    @router.get("/cycles")
    async def cycles(limit: int = Query(50, ge=1, le=500)):
        rows = container.db.query(
            "SELECT id,status,report_json,started_at,finished_at FROM automation_cycles ORDER BY started_at DESC LIMIT ?",
            (limit,),
        )
        for row in rows:
            row["report"] = json.loads(row.pop("report_json"))
        return {"cycles": rows}

    @router.get("/state")
    async def state():
        return {
            "state": container.automation_state.snapshot(),
            "capabilities": container.capabilities.snapshot(),
            "operations": [item.__dict__ if hasattr(item, "__dict__") else {
                "name": item.name, "capability": item.capability, "queue": item.queue,
                "priority": item.priority, "heavy": item.heavy, "risk": item.risk,
                "interval_seconds": item.interval_seconds,
            } for item in container.operation_registry.all()],
        }

    @router.post("/cycle", dependencies=[Depends(authorizer.require)])
    async def run_cycle(force: bool = False):
        return await container.automation.run_cycle(force=force)

    @router.post("/recover", dependencies=[Depends(authorizer.require)])
    async def recover():
        return container.runtime_coordinator.recover()

    return router
