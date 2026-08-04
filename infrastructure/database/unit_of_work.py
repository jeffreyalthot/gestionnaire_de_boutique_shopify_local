from infrastructure.database.engine import Database
class UnitOfWork:
    def __init__(self, db: Database) -> None:
        self.db = db
    def __enter__(self):
        self._context = self.db.transaction()
        self.connection = self._context.__enter__()
        return self
    def __exit__(self, exc_type, exc, tb):
        return self._context.__exit__(exc_type, exc, tb)
