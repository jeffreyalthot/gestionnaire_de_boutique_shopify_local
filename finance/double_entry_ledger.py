from uuid import uuid4
from infrastructure.database.engine import Database,utcnow
class DoubleEntryLedger:
    def __init__(self,db: Database) -> None: self.db=db
    def post(self,transaction_id: str,debit_account: str,credit_account: str,amount: float,
             currency: str="CAD",memo: str="") -> None:
        if amount<0: raise ValueError("Montant négatif.")
        with self.db.transaction() as conn:
            conn.execute("INSERT INTO ledger(id,transaction_id,account,debit,credit,currency,memo,created_at) VALUES(?,?,?,?,?,?,?,?)",
                         (str(uuid4()),transaction_id,debit_account,amount,0,currency,memo,utcnow()))
            conn.execute("INSERT INTO ledger(id,transaction_id,account,debit,credit,currency,memo,created_at) VALUES(?,?,?,?,?,?,?,?)",
                         (str(uuid4()),transaction_id,credit_account,0,amount,currency,memo,utcnow()))
    def balanced(self,transaction_id: str) -> bool:
        row=self.db.query_one("SELECT COALESCE(SUM(debit),0) d,COALESCE(SUM(credit),0) c FROM ledger WHERE transaction_id=?",(transaction_id,))
        return bool(row) and abs(float(row["d"])-float(row["c"]))<0.005
