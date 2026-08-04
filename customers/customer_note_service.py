from __future__ import annotations

from typing import Any


class CustomerNoteService:
    """Stocke uniquement des notes opérationnelles non sensibles dans key_values."""

    def __init__(self, db: Any) -> None:
        self.db = db

    def append(self, customer_id: str, note: str, *, maximum: int = 20) -> None:
        key = f"customer-notes:{customer_id}"
        notes = list(self.db.get_value(key, []))
        sanitized = " ".join(note.replace("\r", " ").replace("\n", " ").split())[:500]
        if sanitized:
            notes.append(sanitized)
        self.db.set_value(key, notes[-max(1, min(maximum, 100)):])

    def list(self, customer_id: str) -> tuple[str, ...]:
        return tuple(self.db.get_value(f"customer-notes:{customer_id}", []))
