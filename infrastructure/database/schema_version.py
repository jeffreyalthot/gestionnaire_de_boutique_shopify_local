from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True,order=True)
class SchemaVersion:
    value: int
    @classmethod
    def read(cls,db: Any)->'SchemaVersion':
        row=db.query_one("SELECT value FROM schema_meta WHERE key='schema_version'")
        return cls(int(row['value']) if row else 0)
