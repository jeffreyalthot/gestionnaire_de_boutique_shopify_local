from __future__ import annotations
import json
from typing import Any


class BaseRepository:
    table = ''
    id_column = 'id'
    allowed_columns: frozenset[str] = frozenset()

    def __init__(self, db: Any) -> None: self.db=db

    def get(self, identifier: str) -> dict[str, Any] | None:
        return self.db.query_one(f'SELECT * FROM {self.table} WHERE {self.id_column}=?',(identifier,))

    def list(self, *, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        limit=max(1,min(limit,1000)); offset=max(0,offset)
        return self.db.query(f'SELECT * FROM {self.table} ORDER BY rowid DESC LIMIT ? OFFSET ?',(limit,offset))

    def update_fields(self, identifier: str, values: dict[str, Any]) -> int:
        clean={k:v for k,v in values.items() if k in self.allowed_columns}
        if not clean: return 0
        columns=', '.join(f'{key}=?' for key in clean)
        serialized=[json.dumps(v,separators=(',',':')) if isinstance(v,(dict,list,tuple)) else v for v in clean.values()]
        return self.db.execute(f'UPDATE {self.table} SET {columns} WHERE {self.id_column}=?',(*serialized,identifier))
