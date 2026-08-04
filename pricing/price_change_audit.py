from infrastructure.database.engine import Database


class PriceChangeAudit:
    def __init__(self, db: Database) -> None: self.db=db
    def record(self, entity_id: str, old: float, new: float, reason: str, actor: str="automation") -> str:
        return self.db.insert_audit("price_changed",actor,{"entity_id":entity_id,"old_cad":old,"new_cad":new,"reason":reason})
