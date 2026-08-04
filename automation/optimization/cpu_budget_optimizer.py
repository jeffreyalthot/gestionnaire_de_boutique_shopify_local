from __future__ import annotations


class CpuBudgetOptimizer:
    def recommend(self, *, cpu_percent: float, cores: int = 2, current_workers: int = 2) -> dict[str, float | int]:
        cores = max(1, min(2, cores))
        if cpu_percent >= 85:
            workers, sleep = 1, 0.25
        elif cpu_percent >= 65:
            workers, sleep = min(current_workers, cores), 0.10
        else:
            workers, sleep = cores, 0.02
        return {"workers": workers, "cooperative_sleep_seconds": sleep}
