from __future__ import annotations

import json
from infrastructure.database.engine import Database, utcnow


class OrderRepository:
    def __init__(self, db: Database) -> None: self.db=db

    def get(self, order_id: str) -> dict[str, object] | None:
        row=self.db.query_one("SELECT * FROM orders WHERE id=? OR shopify_order_id=?",(order_id,order_id))
        if row: row["payload"]=json.loads(row["payload_json"])
        return row

    def update_status(self, order_id: str, *, financial: str | None=None, fulfillment: str | None=None, procurement: str | None=None) -> None:
        assignments=[]; values=[]
        for column,value in (("financial_status",financial),("fulfillment_status",fulfillment),("procurement_status",procurement)):
            if value is not None: assignments.append(f"{column}=?"); values.append(value)
        if not assignments: return
        assignments.append("updated_at=?"); values.extend((utcnow(),order_id,order_id))
        self.db.execute(f"UPDATE orders SET {','.join(assignments)} WHERE id=? OR shopify_order_id=?",tuple(values))

    def list_actionable(self, limit: int=100) -> list[dict[str, object]]:
        return self.db.query("SELECT * FROM orders WHERE financial_status='paid' AND procurement_status IN ('pending','retry') ORDER BY created_at LIMIT ?",(max(1,min(limit,500)),))
