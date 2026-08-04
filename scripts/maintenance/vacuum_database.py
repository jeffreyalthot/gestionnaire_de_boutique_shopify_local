from config.settings import get_settings
from infrastructure.database.engine import Database

db=Database(get_settings().database_path); db.initialize()
with db.connect() as conn:
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)"); conn.execute("VACUUM"); conn.execute("PRAGMA optimize")
print("database_maintenance=completed")
