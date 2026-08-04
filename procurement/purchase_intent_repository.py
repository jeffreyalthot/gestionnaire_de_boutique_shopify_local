from __future__ import annotations

import json, sqlite3
from infrastructure.database.engine import Database, utcnow
from procurement.purchase_intent import PurchaseIntent


class PurchaseIntentRepository:
    def __init__(self, db: Database) -> None: self.db=db
    def create(self, intent: PurchaseIntent) -> bool:
        try:
            self.db.execute("INSERT INTO purchase_intents(id,idempotency_key,order_id,supplier_id,amount_cad,currency,status,payload_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                            (intent.id,intent.idempotency_key,intent.order_id,intent.supplier_id,intent.amount_cad,intent.currency,intent.status,json.dumps({"lines":intent.lines},sort_keys=True,default=str),utcnow(),utcnow()))
            return True
        except sqlite3.IntegrityError: return False
    def get_by_key(self, key: str) -> dict[str,object] | None: return self.db.query_one("SELECT * FROM purchase_intents WHERE idempotency_key=?",(key,))
    def transition(self, intent_id: str, expected: str, target: str, *, external_order_id: str="", error: str="") -> bool:
        return self.db.execute("UPDATE purchase_intents SET status=?,external_order_id=?,error=?,updated_at=? WHERE id=? AND status=?",(target,external_order_id,error,utcnow(),intent_id,expected))==1
