from app.bootstrap import bootstrap
from infrastructure.database.backup import backup_database
if __name__=="__main__":
    app=bootstrap(); print(backup_database(app.container.db))
