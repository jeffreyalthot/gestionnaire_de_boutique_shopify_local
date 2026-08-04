from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from threading import BoundedSemaphore, RLock
from time import monotonic
from typing import Any

import psutil


@dataclass(frozen=True, slots=True)
class RuntimeBudget:
    max_rss_mb: float = 850.0
    max_cpu_percent: float = 75.0
    max_http_concurrency: int = 2
    max_heavy_operations_per_cycle: int = 1
    max_pending_tasks: int = 5000
    max_media_cache_mb: int = 256
    worker_threads: int = 2


class ResourceGovernor:
    """Process budget governor with pressure levels and bounded HTTP slots."""

    def __init__(self, budget: RuntimeBudget) -> None:
        self.budget = budget
        self._process = psutil.Process(os.getpid())
        self._lock = RLock()
        self._heavy_used = 0
        self._cycle_id = ""
        self._http_slots = BoundedSemaphore(max(1, int(budget.max_http_concurrency)))
        self._http_in_use = 0
        self._last_sample: dict[str, Any] = {}
        self._last_sample_at = 0.0

    def begin_cycle(self, cycle_id: str) -> None:
        with self._lock:
            self._cycle_id = cycle_id
            self._heavy_used = 0

    def sample(self, *, cache_seconds: float = 0.1) -> dict[str, Any]:
        now = monotonic()
        with self._lock:
            if self._last_sample and now - self._last_sample_at < max(0.0, cache_seconds):
                return dict(self._last_sample)
            rss_mb = self._process.memory_info().rss / 1048576
            cpu = self._process.cpu_percent(None)
            memory_ratio = rss_mb / max(1.0, self.budget.max_rss_mb)
            cpu_ratio = cpu / max(1.0, self.budget.max_cpu_percent)
            ratio = max(memory_ratio, cpu_ratio)
            pressure = "critical" if ratio >= 1 else ("high" if ratio >= .85 else ("elevated" if ratio >= .70 else "normal"))
            result = {
                "rss_mb": round(rss_mb, 2),
                "cpu_percent": round(cpu, 2),
                "memory_ratio": round(memory_ratio, 4),
                "cpu_ratio": round(cpu_ratio, 4),
                "pressure": pressure,
                "within_memory_budget": rss_mb <= self.budget.max_rss_mb,
                "within_cpu_budget": cpu <= self.budget.max_cpu_percent,
                "cycle_id": self._cycle_id,
                "heavy_used": self._heavy_used,
                "http_in_use": self._http_in_use,
                "budget": asdict(self.budget),
            }
            self._last_sample = result
            self._last_sample_at = now
            return dict(result)

    def allow(self, *, heavy: bool = False, pending_tasks: int = 0) -> tuple[bool, str]:
        with self._lock:
            sample = self.sample(cache_seconds=0.0)
            if not sample["within_memory_budget"]:
                return False, "memory_budget_exceeded"
            if not sample["within_cpu_budget"]:
                return False, "cpu_budget_exceeded"
            if pending_tasks >= self.budget.max_pending_tasks:
                return False, "queue_backpressure"
            if heavy and sample["pressure"] in {"high", "critical"}:
                return False, "resource_pressure"
            if heavy and self._heavy_used >= self.budget.max_heavy_operations_per_cycle:
                return False, "heavy_operation_budget_exhausted"
            if heavy:
                self._heavy_used += 1
                self._last_sample = {}
            return True, "allowed"

    def acquire_http_slot(self, timeout: float = 0.0) -> bool:
        acquired = self._http_slots.acquire(timeout=max(0.0, timeout))
        if acquired:
            with self._lock:
                self._http_in_use += 1
                self._last_sample = {}
        return acquired

    def release_http_slot(self) -> None:
        with self._lock:
            if self._http_in_use <= 0:
                raise RuntimeError("no HTTP slot is currently acquired")
            self._http_in_use -= 1
            self._last_sample = {}
        self._http_slots.release()
