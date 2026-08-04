from __future__ import annotations


class CacheBudgetOptimizer:
    def recommend(self, *, rss_mb: float, rss_limit_mb: float, hit_ratio: float, current_mb: int) -> int:
        headroom = max(0.0, rss_limit_mb - rss_mb)
        if headroom < 128:
            return max(16, int(current_mb * 0.5))
        if hit_ratio < 0.30:
            return max(16, int(current_mb * 0.75))
        if hit_ratio > 0.85 and headroom > 384:
            return min(512, int(current_mb * 1.25))
        return max(16, min(512, current_mb))
