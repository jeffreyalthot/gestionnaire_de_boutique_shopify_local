from __future__ import annotations

from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Awaitable, Callable


@dataclass(frozen=True, slots=True)
class RepositoryCall:
    resource: str
    operation: str
    elapsed_seconds: float
    success: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ShopifyRepository:
    resource = "resource"

    def __init__(self, client: Any) -> None:
        self.client = client
        self.calls = 0
        self.failures = 0
        self.total_seconds = 0.0
        self.last_call: RepositoryCall | None = None

    async def _call(self, operation: str, function: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        started = monotonic(); self.calls += 1
        try:
            value = await function(*args, **kwargs)
        except Exception:
            self.failures += 1
            self.last_call = RepositoryCall(self.resource, operation, monotonic() - started, False)
            self.total_seconds += self.last_call.elapsed_seconds
            raise
        self.last_call = RepositoryCall(self.resource, operation, monotonic() - started, True)
        self.total_seconds += self.last_call.elapsed_seconds
        return value

    def snapshot(self) -> dict[str, object]:
        return {
            "resource": self.resource, "calls": self.calls, "failures": self.failures,
            "total_seconds": round(self.total_seconds, 6),
            "last_call": self.last_call.as_dict() if self.last_call else None,
        }
