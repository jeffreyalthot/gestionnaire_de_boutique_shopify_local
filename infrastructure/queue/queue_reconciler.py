from __future__ import annotations
from datetime import datetime,timezone
from typing import Any
class QueueReconciler:
    def __init__(self,db: Any)->None: self.db=db
    def recover_expired(self)->int:
        now=datetime.now(timezone.utc).isoformat()
        return self.db.execute("UPDATE tasks SET status='pending',worker_id=NULL,lease_until=NULL,updated_at=? WHERE status='leased' AND lease_until<?",(now,now))
