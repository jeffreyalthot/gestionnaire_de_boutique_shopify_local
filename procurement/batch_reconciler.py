from infrastructure.database.engine import Database
class BatchReconciler:
    def __init__(self,db: Database) -> None: self.db=db
    def reconcile(self,batch_id: str) -> dict[str,object]:
        batch=self.db.query_one("SELECT * FROM batches WHERE id=?",(batch_id,))
        orders=self.db.query("SELECT o.* FROM orders o JOIN batch_orders bo ON bo.order_id=o.id WHERE bo.batch_id=?",(batch_id,))
        payments=self.db.query("SELECT * FROM payments WHERE batch_id=?",(batch_id,))
        return {"batch":batch,"orders":orders,"payments":payments,
                "balanced":bool(batch) and len(orders)==int(batch.get("order_count",0))}
