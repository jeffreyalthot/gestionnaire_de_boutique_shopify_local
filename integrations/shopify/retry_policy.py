from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from infrastructure.http.backoff import BackoffPolicy


RETRYABLE_STATUSES = frozenset({408, 409, 425, 429, 500, 502, 503, 504})


@dataclass(frozen=True, slots=True)
class ShopifyRetryDecision:
    retry: bool
    delay_seconds: float
    reason: str


def decide_retry(attempt: int, *, status_code: int = 0, headers: Mapping[str, str] | None = None, network_error: bool = False) -> ShopifyRetryDecision:
    headers_value = {str(key).lower(): str(value) for key, value in (headers or {}).items()}
    retry_after = None
    try:
        retry_after = float(headers_value.get("retry-after", ""))
    except ValueError:
        pass
    retryable = network_error or status_code in RETRYABLE_STATUSES
    delay = BackoffPolicy(0.75, 45.0, 0.2, 2.0).delay(attempt, retry_after=retry_after) if retryable else 0.0
    reason = "network_error" if network_error else f"http_{status_code}" if retryable else "not_retryable"
    return ShopifyRetryDecision(retryable, delay, reason)


def retry_delay(attempt: int) -> float:
    return BackoffPolicy(0.75, 45.0).delay(attempt)
