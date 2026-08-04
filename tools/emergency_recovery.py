from app.bootstrap import bootstrap
from infrastructure.database.backup import backup_database
def run() -> dict[str,object]:
    app=bootstrap(); recovered=app.container.db.purge_expired_leases(); backup=backup_database(app.container.db)
    return {"recovered_leases":recovered,"backup":str(backup)}
if __name__=="__main__": print(run())
