from __future__ import annotations
from dataclasses import asdict,dataclass
from typing import Any

@dataclass(frozen=True)
class IntegrityReport:
    quick_check: str
    foreign_key_errors: int
    journal_mode: str
    ok: bool
    def as_dict(self): return asdict(self)

class IntegrityChecker:
    def __init__(self,db: Any)->None: self.db=db
    def run(self)->IntegrityReport:
        with self.db.connect() as conn:
            quick=str(conn.execute('PRAGMA quick_check').fetchone()[0])
            fk=len(conn.execute('PRAGMA foreign_key_check').fetchall())
            journal=str(conn.execute('PRAGMA journal_mode').fetchone()[0])
        return IntegrityReport(quick,fk,journal,quick=='ok' and fk==0)
