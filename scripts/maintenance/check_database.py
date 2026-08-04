from config.settings import get_settings
from infrastructure.database.engine import Database

db=Database(get_settings().database_path); db.initialize()
with db.connect() as conn:
    print({"quick_check":conn.execute("PRAGMA quick_check").fetchone()[0],"integrity_check":conn.execute("PRAGMA integrity_check").fetchone()[0],"counts":db.counts(),"audit":db.verify_audit_chain()})
