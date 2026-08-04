from contextvars import ContextVar
from uuid import uuid4
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
def ensure_correlation_id(value: str | None = None) -> str:
    current = value or correlation_id.get() or str(uuid4())
    correlation_id.set(current)
    return current
