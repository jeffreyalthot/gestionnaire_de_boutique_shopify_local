from __future__ import annotations


class ScheduleOptimizer:
    def recommend_interval(self, *, base_seconds: int, backlog: int, error_rate: float, unchanged_cycles: int) -> int:
        interval = max(10, base_seconds)
        if error_rate > 0.10:
            interval *= 2
        elif backlog > 1000:
            interval = max(10, interval // 4)
        elif backlog > 100:
            interval = max(10, interval // 2)
        elif unchanged_cycles >= 10:
            interval = min(3600, interval * 2)
        return int(max(10, min(3600, interval)))
