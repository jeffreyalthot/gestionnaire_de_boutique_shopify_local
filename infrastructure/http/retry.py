from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Generic, TypeVar

from infrastructure.http.backoff import BackoffPolicy

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RetryAttempt:
    attempt: int
    delay_seconds: float
    error_type: str
    message: str


@dataclass(frozen=True, slots=True)
class RetryOutcome(Generic[T]):
    value: T
    attempts: int
    duration_seconds: float
    history: tuple[RetryAttempt, ...]

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["value"] = self.value
        return data


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    attempts: int = 3
    retryable_exceptions: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError)
    backoff: BackoffPolicy = BackoffPolicy()

    def should_retry(self, exception: BaseException, attempt: int) -> bool:
        return attempt < max(0, self.attempts) and isinstance(exception, self.retryable_exceptions)


async def execute_with_retry(
    action: Callable[[], Awaitable[T]],
    policy: RetryPolicy,
    *,
    retry_after: Callable[[BaseException], float | None] | None = None,
    on_retry: Callable[[RetryAttempt], object] | None = None,
) -> RetryOutcome[T]:
    started = monotonic()
    history: list[RetryAttempt] = []
    attempt = 0
    while True:
        try:
            value = await action()
            return RetryOutcome(value, attempt + 1, round(monotonic() - started, 6), tuple(history))
        except asyncio.CancelledError:
            raise
        except BaseException as exc:
            if not policy.should_retry(exc, attempt):
                raise
            hinted = retry_after(exc) if retry_after else None
            delay = policy.backoff.delay(attempt, retry_after=hinted)
            record = RetryAttempt(attempt + 1, delay, type(exc).__name__, str(exc)[:300])
            history.append(record)
            if on_retry:
                on_retry(record)
            await asyncio.sleep(delay)
            attempt += 1


async def retry_async(
    action: Callable[[], Awaitable[T]],
    attempts: int,
    *,
    retryable_exceptions: Iterable[type[BaseException]] = (Exception,),
) -> T:
    """API historique: ``attempts`` correspond au nombre de reprises après l'essai initial."""
    policy = RetryPolicy(max(0, int(attempts)), tuple(retryable_exceptions), BackoffPolicy())
    return (await execute_with_retry(action, policy)).value
