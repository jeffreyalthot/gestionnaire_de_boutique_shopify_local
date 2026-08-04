from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic


@dataclass(frozen=True, slots=True)
class AlibabaRateLimitSnapshot:
    rate: float
    burst: int
    tokens: float
    waited_seconds: float
    requests: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AlibabaRateLimitManager:
    """Async token bucket that supports small bursts without extra threads."""

    def __init__(self, requests_per_second: float = 2, burst: int = 2) -> None:
        self.rate = max(float(requests_per_second), 0.1)
        self.burst = max(1, int(burst))
        self.tokens = float(self.burst)
        self.updated_at = monotonic()
        self._lock = asyncio.Lock()
        self.waited_seconds = 0.0
        self.requests = 0

    async def wait(self, cost: float = 1.0) -> float:
        cost = max(0.01, float(cost))
        waited = 0.0
        async with self._lock:
            while True:
                now = monotonic()
                self.tokens = min(self.burst, self.tokens + (now - self.updated_at) * self.rate)
                self.updated_at = now
                if self.tokens >= cost:
                    self.tokens -= cost
                    self.requests += 1
                    self.waited_seconds += waited
                    return waited
                delay = (cost - self.tokens) / self.rate
                await asyncio.sleep(delay)
                waited += delay

    def snapshot(self) -> AlibabaRateLimitSnapshot:
        return AlibabaRateLimitSnapshot(self.rate, self.burst, round(self.tokens, 4), round(self.waited_seconds, 6), self.requests)
