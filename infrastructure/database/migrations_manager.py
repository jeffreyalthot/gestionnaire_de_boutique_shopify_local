from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable

@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable[[Any],None]

class MigrationsManager:
    def __init__(self,db: Any)->None: self.db=db; self._migrations={}
    def register(self,migration: Migration)->None:
        if migration.version in self._migrations: raise ValueError('Version de migration dupliquée.')
        self._migrations[migration.version]=migration
    def current_version(self)->int:
        row=self.db.query_one("SELECT value FROM schema_meta WHERE key='schema_version'")
        return int(row['value']) if row else 0
    def migrate(self,target: int|None=None)->list[str]:
        applied=[]; current=self.current_version(); target=target or max(self._migrations,default=current)
        with self.db.transaction() as conn:
            for version in sorted(self._migrations):
                if current<version<=target:
                    self._migrations[version].apply(conn)
                    conn.execute("INSERT INTO schema_meta(key,value) VALUES('schema_version',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(str(version),))
                    applied.append(self._migrations[version].name)
        return applied
