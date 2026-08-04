from __future__ import annotations


class MemoryBudgetOptimizer:
    def recommend(self, *, rss_mb: float, limit_mb: float, queue_depth: int) -> dict[str, int | bool]:
        ratio = rss_mb / max(1.0, limit_mb)
        if ratio >= 0.90:
            return {"pause_heavy": True, "page_size": 10, "queue_claim": 1}
        if ratio >= 0.75:
            return {"pause_heavy": True, "page_size": 20, "queue_claim": 2}
        return {"pause_heavy": False, "page_size": min(50, max(10, 10 + queue_depth // 100)), "queue_claim": 4}
