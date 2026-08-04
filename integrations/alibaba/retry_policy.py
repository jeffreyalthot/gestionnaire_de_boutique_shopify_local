from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from infrastructure.http.backoff import BackoffPolicy


RETRYABLE_CODES = frozenset({"isp.SYSTEM_ERROR", "isp.TIMEOUT", "isv.SYSTEM_BUSY", "THROTTLED", "SERVICE_UNAVAILABLE"})


@dataclass(frozen=True, slots=True)
class AlibabaRetryDecision:
    retry: bool
    delay_seconds: float
    reason: str


def decide_retry(attempt: int, *, error_code: str = "", headers: Mapping[str, str] | None = None, network_error: bool = False) -> AlibabaRetryDecision:
    normalized = str(error_code).strip()
    retryable = network_error or normalized in RETRYABLE_CODES
    retry_after = None
    header_values = {str(key).lower(): str(value) for key, value in (headers or {}).items()}
    try:
        retry_after = float(header_values.get("retry-after", ""))
    except ValueError:
        pass
    delay = BackoffPolicy(1.0, 60.0, 0.25, 2.0).delay(attempt, retry_after=retry_after) if retryable else 0.0
    return AlibabaRetryDecision(retryable, delay, "network_error" if network_error else normalized or "not_retryable")


def retry_delay(attempt: int) -> float:
    return BackoffPolicy(1.0, 60.0).delay(attempt)
