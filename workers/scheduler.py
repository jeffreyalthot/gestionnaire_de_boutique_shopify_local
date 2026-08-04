from __future__ import annotations

from dataclasses import asdict, dataclass

from infrastructure.scheduler.scheduler import AsyncScheduler


@dataclass(frozen=True, slots=True)
class WorkerScheduleProfile:
    maximum_concurrency: int = 1
    polling_seconds: float = 1.0
    heavy_jobs_per_cycle: int = 1

    def __post_init__(self) -> None:
        if not 1 <= self.maximum_concurrency <= 2: raise ValueError("concurrence invalide pour le profil 2 Go")

    def as_dict(self) -> dict[str, object]: return asdict(self)


__all__ = ["AsyncScheduler", "WorkerScheduleProfile"]
