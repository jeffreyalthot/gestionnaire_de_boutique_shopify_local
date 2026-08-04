from __future__ import annotations

import random
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class BackoffPolicy:
    base_seconds: float = 0.5
    maximum_seconds: float = 30.0
    jitter_ratio: float = 0.2
    multiplier: float = 2.0

    def delay(self, attempt: int, *, retry_after: float | None = None, rng: random.Random | None = None) -> float:
        if retry_after is not None and retry_after >= 0:
            return min(self.maximum_seconds, float(retry_after))
        raw = min(self.maximum_seconds, self.base_seconds * (self.multiplier ** max(0, int(attempt))))
        generator = rng or random
        jitter = raw * max(0.0, self.jitter_ratio)
        return round(max(0.0, generator.uniform(raw - jitter, raw + jitter)), 4)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def exponential_backoff(attempt: int, base: float = 0.5, maximum: float = 30) -> float:
    return BackoffPolicy(base, maximum).delay(attempt)
