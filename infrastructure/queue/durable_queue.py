from __future__ import annotations
import json
from datetime import datetime,timedelta,timezone
from typing import Any,Iterable
from uuid import uuid4
from infrastructure.database.engine import Database,utcnow
from infrastructure.queue.task import QueueTask
class DurableQueue:
    def __init__(self,db: Database) -> None:self.db=db
    def enqueue(self,task_type: str,payload: dict[str,Any],idempotency_key: str,queue: str="default",priority: int=100,delay_seconds: float=0,max_attempts: int=8) -> str:
        if not task_type or not idempotency_key:raise ValueError("task_type et idempotency_key requis")
        existing=self.db.query_one("SELECT id FROM tasks WHERE idempotency_key=?",(idempotency_key,))
        if existing:return str(existing["id"])
        task_id=str(uuid4());available=(datetime.now(timezone.utc)+timedelta(seconds=max(0,delay_seconds))).isoformat();now=utcnow()
        self.db.execute("INSERT INTO tasks(id,queue,task_type,payload_json,priority,status,attempts,max_attempts,available_at,idempotency_key,created_at,updated_at) VALUES(?,?,?,?,?,'pending',0,?,?,?,?,?)",(task_id,queue,task_type,json.dumps(payload,ensure_ascii=False,default=str,separators=(",",":")),int(priority),max(1,int(max_attempts)),available,idempotency_key,now,now));return task_id
    def enqueue_many(self,tasks: Iterable[dict[str,Any]]) -> tuple[str,...]:
        return tuple(self.enqueue(str(t["task_type"]),dict(t.get("payload",{})),str(t["idempotency_key"]),str(t.get("queue","default")),int(t.get("priority",100)),float(t.get("delay_seconds",0)),int(t.get("max_attempts",8))) for t in tasks)
    def claim(self,worker_id: str,queues: tuple[str,...]=("default",),lease_seconds: int=120) -> QueueTask | None:
        if not queues:raise ValueError("au moins une file requise")
        self.db.purge_expired_leases();placeholders=",".join("?" for _ in queues)
        with self.db.transaction() as conn:
            row=conn.execute(f"SELECT * FROM tasks WHERE status='pending' AND queue IN ({placeholders}) AND available_at<=? ORDER BY priority ASC,created_at ASC LIMIT 1",(*queues,utcnow())).fetchone()
            if row is None:return None
            lease_until=(datetime.now(timezone.utc)+timedelta(seconds=max(1,lease_seconds))).isoformat();changed=conn.execute("UPDATE tasks SET status='leased',worker_id=?,lease_until=?,updated_at=? WHERE id=? AND status='pending'",(worker_id,lease_until,utcnow(),row["id"])).rowcount
            if changed!=1:return None
            return QueueTask(id=row["id"],queue=row["queue"],task_type=row["task_type"],payload=json.loads(row["payload_json"]),priority=row["priority"],attempts=row["attempts"],max_attempts=row["max_attempts"],idempotency_key=row["idempotency_key"])
    def claim_many(self,worker_id: str,queues: tuple[str,...]=("default",),limit: int=10,lease_seconds: int=120) -> tuple[QueueTask,...]:
        rows=[]
        for _ in range(max(1,min(int(limit),100))):
            task=self.claim(worker_id,queues,lease_seconds)
            if task is None:break
            rows.append(task)
        return tuple(rows)
    def heartbeat(self,task_id: str,worker_id: str,lease_seconds: int=120) -> bool:
        lease=(datetime.now(timezone.utc)+timedelta(seconds=max(1,lease_seconds))).isoformat();return bool(self.db.execute("UPDATE tasks SET lease_until=?,updated_at=? WHERE id=? AND status='leased' AND worker_id=?",(lease,utcnow(),task_id,worker_id)))
    def complete(self,task_id: str) -> None:self.db.execute("UPDATE tasks SET status='completed',worker_id=NULL,lease_until=NULL,updated_at=? WHERE id=?",(utcnow(),task_id))
    def cancel(self,task_id: str,reason: str="cancelled") -> bool:return bool(self.db.execute("UPDATE tasks SET status='cancelled',error=?,worker_id=NULL,lease_until=NULL,updated_at=? WHERE id=? AND status IN ('pending','leased')",(reason[:4000],utcnow(),task_id)))
    def fail(self,task: QueueTask,error: str,base_delay_seconds: float=5) -> str:
        attempts=task.attempts+1
        if attempts>=task.max_attempts:status="dead";available=utcnow()
        else:status="pending";delay=min(max(.1,base_delay_seconds)*(2**min(attempts,8)),3600);available=(datetime.now(timezone.utc)+timedelta(seconds=delay)).isoformat()
        self.db.execute("UPDATE tasks SET status=?,attempts=?,available_at=?,worker_id=NULL,lease_until=NULL,error=?,updated_at=? WHERE id=?",(status,attempts,available,error[:4000],utcnow(),task.id));return status
    def retry_dead(self,task_id: str) -> None:self.db.execute("UPDATE tasks SET status='pending',attempts=0,error='',available_at=?,updated_at=? WHERE id=? AND status='dead'",(utcnow(),utcnow(),task_id))
    def purge_completed(self,older_than_seconds: int=86400,limit: int=10000) -> int:
        cutoff=(datetime.now(timezone.utc)-timedelta(seconds=max(0,older_than_seconds))).isoformat();ids=[r["id"] for r in self.db.query("SELECT id FROM tasks WHERE status IN ('completed','cancelled','discarded') AND updated_at<? ORDER BY updated_at LIMIT ?",(cutoff,max(1,min(limit,50000))))]
        if not ids:return 0
        placeholders=",".join("?" for _ in ids);return int(self.db.execute(f"DELETE FROM tasks WHERE id IN ({placeholders})",tuple(ids)) or 0)
    def stats(self) -> dict[str,int]:return {str(r["status"]):int(r["count"]) for r in self.db.query("SELECT status,COUNT(*) count FROM tasks GROUP BY status")}
    def stats_by_queue(self) -> dict[str,dict[str,int]]:
        result={}
        for row in self.db.query("SELECT queue,status,COUNT(*) count FROM tasks GROUP BY queue,status"):result.setdefault(str(row["queue"]),{})[str(row["status"])]=int(row["count"])
        return result
