from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
class Decision(BaseModel):
    approved: bool
    actor: str
    reason: str=""
def router_for(db,gate):
    router=APIRouter()
    @router.get("/approvals")
    async def approvals(): return db.query("SELECT * FROM approvals ORDER BY requested_at DESC LIMIT 100")
    @router.post("/approvals/{approval_id}/decision")
    async def decide(approval_id: str,decision: Decision):
        row=db.query_one("SELECT * FROM approvals WHERE id=?",(approval_id,))
        if not row: raise HTTPException(404,"Approbation introuvable.")
        gate.decide(approval_id,decision.approved,decision.actor,decision.reason)
        return {"status":"approved" if decision.approved else "rejected"}
    return router
