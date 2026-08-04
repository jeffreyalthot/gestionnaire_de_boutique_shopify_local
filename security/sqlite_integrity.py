from __future__ import annotations

from typing import Any


def sqlite_integrity(db: Any) -> dict[str, object]:
    with db.connect() as conn:
        quick=str(conn.execute("PRAGMA quick_check").fetchone()[0])
        foreign=list(conn.execute("PRAGMA foreign_key_check").fetchmany(100))
        wal=list(conn.execute("PRAGMA wal_checkpoint(PASSIVE)").fetchone())
    return {"ok":quick.lower()=="ok" and not foreign,"quick_check":quick,"foreign_key_errors":len(foreign),"wal":wal}
