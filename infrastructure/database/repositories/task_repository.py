from infrastructure.database.engine import Database
class TaskRepository:
    table="tasks"
    def __init__(self,db: Database) -> None: self.db=db
    def get(self,record_id: str) -> dict[str,object]|None: return self.db.query_one(f"SELECT * FROM {self.table} WHERE id=?",(record_id,))
    def all(self,limit: int=100) -> list[dict[str,object]]: return self.db.query(f"SELECT * FROM {self.table} ORDER BY rowid DESC LIMIT ?",(limit,))
    def delete(self,record_id: str) -> int: return self.db.execute(f"DELETE FROM {self.table} WHERE id=?",(record_id,))
