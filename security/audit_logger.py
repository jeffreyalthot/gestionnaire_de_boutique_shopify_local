from infrastructure.database.engine import Database
class AuditLogger:
    def __init__(self, db: Database) -> None:
        self.db = db
    def record(self, action: str, actor: str, detail: dict[str, object]) -> None:
        self.db.insert_audit(action, actor, detail)
