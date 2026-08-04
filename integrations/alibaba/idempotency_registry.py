from __future__ import annotations
from datetime import datetime,timezone
from typing import Any
class AlibabaIdempotencyRegistry:
    def __init__(self,db: Any)->None:self.db=db
    def reserve(self,key: str,operation: str,payload_hash: str)->bool:
        if not key:return False
        return bool(self.db.execute("INSERT OR IGNORE INTO automation_actions(id,idempotency_key,name,status,result_json,error,updated_at) VALUES(?,?,?,?,?,?,?)",(key,key,f'alibaba:{operation}','reserved','{}','',datetime.now(timezone.utc).isoformat())))
    def complete(self,key: str,result: dict)->None:self.db.execute("UPDATE automation_actions SET status='completed',result_json=?,updated_at=? WHERE idempotency_key=?",(json_dumps(result),datetime.now(timezone.utc).isoformat(),key))
def json_dumps(value):
    import json;return json.dumps(value,ensure_ascii=False,separators=(',',':'))
