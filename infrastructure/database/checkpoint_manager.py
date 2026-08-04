from __future__ import annotations
import json
from datetime import datetime, timezone
from typing import Any


class CheckpointManager:
    def __init__(self, db: Any) -> None: self.db=db
    def save(self,name: str,cursor: str='',status: str='running',detail: dict[str,Any]|None=None)->None:
        now=datetime.now(timezone.utc).isoformat()
        self.db.execute("INSERT INTO reconciliation_checkpoints(name,cursor,status,detail_json,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(name) DO UPDATE SET cursor=excluded.cursor,status=excluded.status,detail_json=excluded.detail_json,updated_at=excluded.updated_at",(name,cursor,status,json.dumps(detail or {},separators=(',',':')),now))
    def load(self,name: str)->dict[str,Any]|None:
        row=self.db.query_one('SELECT * FROM reconciliation_checkpoints WHERE name=?',(name,))
        if row: row['detail']=json.loads(row.pop('detail_json'))
        return row
    def complete(self,name: str,cursor: str='',detail: dict[str,Any]|None=None)->None: self.save(name,cursor,'completed',detail)
