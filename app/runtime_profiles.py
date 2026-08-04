from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    name: str
    rss_mb: int
    workers: int
    http_concurrency: int
    refresh_hz: float
    cache_mb: int


PROFILES = {
    "lite_2gb": RuntimeProfile("lite_2gb", 850, 2, 2, 2.0, 256),
    "minimal_2gb": RuntimeProfile("minimal_2gb", 650, 1, 1, 1.0, 128),
    "balanced": RuntimeProfile("balanced", 1200, 2, 2, 4.0, 384),
}


def get_runtime_profile(name: str) -> RuntimeProfile:
    return PROFILES.get(name, PROFILES["lite_2gb"])
