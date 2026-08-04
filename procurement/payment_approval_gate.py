from uuid import uuid4
from infrastructure.database.engine import Database,utcnow
class PaymentApprovalGate:
    def __init__(self,db: Database,required: bool=True) -> None: self.db=db; self.required=required
    def request(self,batch_id: str,amount_cad: float) -> str:
        if not self.required: return "automatic"
        existing=self.db.query_one("SELECT * FROM approvals WHERE entity_type='batch' AND entity_id=? ORDER BY requested_at DESC LIMIT 1",(batch_id,))
        if existing: return str(existing["id"])
        approval_id=str(uuid4())
        self.db.execute("INSERT INTO approvals(id,action,entity_type,entity_id,amount_cad,status,requested_at) VALUES(?,'pay_alibaba_batch','batch',?,?,'pending',?)",
                        (approval_id,batch_id,amount_cad,utcnow()))
        return approval_id
    def approved(self,batch_id: str) -> bool:
        if not self.required: return True
        return bool(self.db.scalar("SELECT COUNT(*) FROM approvals WHERE entity_type='batch' AND entity_id=? AND status='approved'",(batch_id,),0))
    def decide(self,approval_id: str,approved: bool,actor: str,reason: str="") -> None:
        status="approved" if approved else "rejected"
        self.db.execute("UPDATE approvals SET status=?,decided_at=?,decided_by=?,reason=? WHERE id=? AND status='pending'",
                        (status,utcnow(),actor,reason,approval_id))
