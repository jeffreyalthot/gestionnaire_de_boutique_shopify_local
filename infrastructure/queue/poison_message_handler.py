from __future__ import annotations
from typing import Any
class PoisonMessageHandler:
    def __init__(self,db: Any)->None: self.db=db
    def quarantine(self,task: Any,error: str)->None:
        self.db.execute("UPDATE tasks SET status='dead',error=?,updated_at=datetime('now') WHERE id=?",(error[:4000],task.id))
        self.db.insert_audit('queue.poison','worker',{'task_id':task.id,'task_type':task.task_type,'error':error[:1000]})
