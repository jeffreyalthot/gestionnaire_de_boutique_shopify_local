from __future__ import annotations
import json
from infrastructure.database.engine import Database,utcnow

def dead_letters(db: Database,limit: int=100,queue: str="") -> list[dict[str,object]]:
    if queue:return db.query("SELECT * FROM tasks WHERE status='dead' AND queue=? ORDER BY updated_at DESC LIMIT ?",(queue,max(1,min(limit,1000))))
    return db.query("SELECT * FROM tasks WHERE status='dead' ORDER BY updated_at DESC LIMIT ?",(max(1,min(limit,1000)),))
class DeadLetterQueue:
    def __init__(self,db: Database) -> None:self.db=db
    def list(self,limit: int=100,queue: str=""):return dead_letters(self.db,limit,queue)
    def replay(self,task_id: str,reset_attempts: bool=True) -> bool:
        attempts=0 if reset_attempts else self.db.scalar("SELECT attempts FROM tasks WHERE id=?",(task_id,),default=0)
        changed=self.db.execute("UPDATE tasks SET status='pending',attempts=?,error='',available_at=?,worker_id=NULL,lease_until=NULL,updated_at=? WHERE id=? AND status='dead'",(attempts,utcnow(),utcnow(),task_id))
        return bool(changed)
    def discard(self,task_id: str,reason: str="operator_discard") -> bool:
        changed=self.db.execute("UPDATE tasks SET status='discarded',error=?,updated_at=? WHERE id=? AND status='dead'",(reason[:4000],utcnow(),task_id));return bool(changed)
    def export(self,limit: int=1000) -> str:return json.dumps(self.list(limit),ensure_ascii=False,default=str)
