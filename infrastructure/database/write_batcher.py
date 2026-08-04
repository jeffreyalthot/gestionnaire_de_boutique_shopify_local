from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Iterable,Sequence
@dataclass(frozen=True)
class WriteOperation:
    sql: str
    parameters: Sequence[Any]
class WriteBatcher:
    def __init__(self,db: Any,max_operations: int=500)->None: self.db=db; self.max_operations=max_operations
    def execute(self,operations: Iterable[WriteOperation])->int:
        items=list(operations)
        if len(items)>self.max_operations: raise ValueError('Lot SQLite trop volumineux.')
        with self.db.transaction() as conn:
            for item in items: conn.execute(item.sql,tuple(item.parameters))
        return len(items)
