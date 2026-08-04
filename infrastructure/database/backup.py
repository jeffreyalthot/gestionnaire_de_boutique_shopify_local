from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from infrastructure.database.engine import Database
from config.paths import BACKUP_DIR

def backup_database(db: Database, destination: Path | None = None) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    target = destination or BACKUP_DIR / f"orchestrator-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}.db"
    with db.connect() as source, sqlite3.connect(target) as dest:
        source.backup(dest)
    return target
