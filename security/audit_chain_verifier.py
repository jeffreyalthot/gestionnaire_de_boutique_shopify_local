from infrastructure.database.engine import Database


class AuditChainVerifier:
    def __init__(self, db: Database) -> None: self.db=db
    def verify(self) -> dict[str,object]: return self.db.verify_audit_chain()
