from collections.abc import Callable
from typing import TypeVar
from infrastructure.database.engine import Database
T = TypeVar("T")
def execute_once(db: Database, key: str, action: Callable[[], T]) -> T | None:
    marker = f"idempotency:{key}"
    if db.get_value(marker, False):
        return None
    result = action()
    db.set_value(marker, True)
    return result
