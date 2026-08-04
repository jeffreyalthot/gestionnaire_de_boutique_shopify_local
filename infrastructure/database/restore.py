from pathlib import Path
import shutil
from infrastructure.database.engine import Database

def restore_database(db: Database, backup_path: Path) -> None:
    if not backup_path.is_file():
        raise FileNotFoundError(backup_path)
    shutil.copy2(backup_path, db.path)
    db.initialize()
