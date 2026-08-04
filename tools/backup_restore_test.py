from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

import sqlite3
import tempfile
from pathlib import Path
from tools.runtime_tool import database, emit
from infrastructure.database.backup import backup_database


def main() -> int:
    _, db = database()
    target = Path(tempfile.mkdtemp()) / "orchestrator-backup.db"
    path = backup_database(db, target)
    ok = path.is_file()
    if ok:
        with sqlite3.connect(path) as connection:
            connection.execute("PRAGMA quick_check").fetchone()
    return emit({"backup": str(path), "exists": ok}, 0 if ok else 2)


if __name__ == "__main__":
    raise SystemExit(main())
