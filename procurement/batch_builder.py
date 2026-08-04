from __future__ import annotations
from datetime import datetime,timezone
from uuid import uuid4
from infrastructure.database.engine import Database,utcnow

class BatchBuilder:
    def __init__(self,db: Database) -> None: self.db=db
    def get_or_create_open_batch(self) -> dict[str,object]:
        row=self.db.query_one("SELECT * FROM batches WHERE status='open' ORDER BY created_at LIMIT 1")
        if row: return row
        batch_id=str(uuid4()); now=utcnow()
        self.db.execute("INSERT INTO batches(id,status,total_cad,order_count,supplier_count,created_at,updated_at) VALUES(?,'open',0,0,0,?,?)",
                        (batch_id,now,now))
        return self.db.query_one("SELECT * FROM batches WHERE id=?",(batch_id,)) or {}
    def add_order(self,batch_id: str,order_id: str,supplier_id: str,amount_cad: float) -> None:
        with self.db.transaction() as conn:
            conn.execute("INSERT OR IGNORE INTO batch_orders(batch_id,order_id,supplier_id,amount_cad) VALUES(?,?,?,?)",
                         (batch_id,order_id,supplier_id,amount_cad))
            conn.execute("UPDATE orders SET procurement_status='batched',updated_at=? WHERE id=?",(utcnow(),order_id))
            totals=conn.execute("SELECT COALESCE(SUM(amount_cad),0),COUNT(*),COUNT(DISTINCT supplier_id) FROM batch_orders WHERE batch_id=?",
                                (batch_id,)).fetchone()
            conn.execute("UPDATE batches SET total_cad=?,order_count=?,supplier_count=?,updated_at=? WHERE id=?",
                         (totals[0],totals[1],totals[2],utcnow(),batch_id))
    def ready_orders(self) -> list[dict[str,object]]:
        return self.db.query("SELECT * FROM orders WHERE financial_status='paid' AND procurement_status='pending' ORDER BY created_at")
