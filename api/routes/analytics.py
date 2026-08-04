from __future__ import annotations

from fastapi import APIRouter, Query


def router_for(container):
    router = APIRouter(prefix="/analytics", tags=["analytics"])

    @router.get("/metric/{metric}")
    async def metric(metric: str, limit: int = Query(100, ge=1, le=1000)):
        return {"metric": metric, "series": container.analytics.series(metric, limit=limit)}

    @router.get("/scorecard")
    async def scorecard():
        from analytics.scorecards.store_scorecard import StoreScorecard
        state = container.dashboard_state()
        counts = state["counts"]
        finance = state["finance"]
        queue = state["queue"]
        revenue = max(1.0, float(finance["revenue"]))
        metrics = {
            "profitability": max(0.0, min(1.0, float(finance["profit"]) / revenue)),
            "fulfillment": 1.0 - min(1.0, float(counts.get("pending_procurement", 0)) / max(1, counts.get("orders", 0))),
            "customer": 1.0 - min(1.0, float(queue.get("dead", 0)) / 10.0),
            "compliance": 1.0 if state["audit"].get("ok") else 0.0,
            "reliability": 1.0 if state["api"]["database"].get("ok") else 0.0,
        }
        return StoreScorecard().build(metrics).as_dict()

    return router
