import argparse
from pathlib import Path
from app.bootstrap import bootstrap
from infrastructure.database.restore import restore_database
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("backup"); a=p.parse_args()
    app=bootstrap(); restore_database(app.container.db,Path(a.backup)); print(app.container.db.health())
