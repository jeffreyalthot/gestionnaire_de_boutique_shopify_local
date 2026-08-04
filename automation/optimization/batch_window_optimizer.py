from __future__ import annotations


class BatchWindowOptimizer:
    def recommend(self, *, pending: int, oldest_age_seconds: float, cpu_percent: float, base_batch: int = 25) -> dict[str, int | str]:
        if pending <= 0:
            return {"batch_size": 0, "delay_seconds": 60, "reason": "empty"}
        pressure = min(4.0, 1.0 + pending / max(1, base_batch * 4))
        cpu_factor = 0.5 if cpu_percent >= 80 else (0.75 if cpu_percent >= 60 else 1.0)
        age_factor = 1.5 if oldest_age_seconds >= 900 else 1.0
        batch = max(1, min(200, int(base_batch * pressure * cpu_factor * age_factor)))
        delay = 1 if pending > batch else (5 if oldest_age_seconds > 60 else 15)
        return {"batch_size": batch, "delay_seconds": delay, "reason": "adaptive"}
