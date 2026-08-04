from __future__ import annotations

import json
from uuid import uuid4

from infrastructure.database.engine import Database, utcnow


class OrderTimeline:
    def __init__(self, db: Database) -> None: self.db=db

    def append(self, order_id: str, event_type: str, *, status: str="", detail: dict[str, object] | None=None) -> str:
        event_id=str(uuid4())
        self.db.execute("INSERT INTO order_timelines(id,order_id,event_type,status,detail_json,occurred_at) VALUES(?,?,?,?,?,?)",
                        (event_id,order_id,event_type,status,json.dumps(detail or {},sort_keys=True,default=str),utcnow()))
        return event_id

    def list(self, order_id: str) -> list[dict[str, object]]:
        rows=self.db.query("SELECT * FROM order_timelines WHERE order_id=? ORDER BY occurred_at,id",(order_id,))
        for row in rows: row["detail"]=json.loads(row.pop("detail_json"))
        return rows
