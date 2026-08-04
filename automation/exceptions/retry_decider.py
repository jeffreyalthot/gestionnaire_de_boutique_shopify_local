from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True, slots=True)
class RetryDecision:
    retry: bool
    delay_seconds: float
    reason: str


class RetryDecider:
    def __init__(self, *, base_seconds: float = 2.0, maximum_seconds: float = 300.0, max_attempts: int = 8) -> None:
        self.base = max(0.1, base_seconds)
        self.maximum = max(self.base, maximum_seconds)
        self.max_attempts = max(1, max_attempts)

    def decide(self, *, retryable: bool, attempts: int, retry_after: float | None = None) -> RetryDecision:
        if not retryable:
            return RetryDecision(False, 0.0, "not_retryable")
        if attempts >= self.max_attempts:
            return RetryDecision(False, 0.0, "attempt_limit")
        if retry_after is not None:
            delay = max(0.0, min(self.maximum, float(retry_after)))
            return RetryDecision(True, delay, "server_retry_after")
        ceiling = min(self.maximum, self.base * (2 ** max(0, attempts)))
        delay = random.uniform(ceiling * 0.5, ceiling)
        return RetryDecision(True, round(delay, 3), "exponential_jitter")
