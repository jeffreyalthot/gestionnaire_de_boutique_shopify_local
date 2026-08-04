from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


class TransactionBoundary:
    def __init__(self, db: Any, *, audit_action: str = "automation.transaction") -> None:
        self.db = db
        self.audit_action = audit_action

    @contextmanager
    def open(self, *, actor: str, detail: dict[str, Any] | None = None) -> Iterator[Any]:
        with self.db.transaction() as connection:
            yield connection
        self.db.insert_audit(self.audit_action, actor, detail or {})
