from __future__ import annotations


class HttpConcurrencyOptimizer:
    def recommend(self, *, rate_limit_remaining: float, error_rate: float, latency_ms: float, maximum: int = 2) -> int:
        maximum = max(1, min(2, maximum))
        if rate_limit_remaining < 0.20 or error_rate > 0.05 or latency_ms > 3000:
            return 1
        return maximum
