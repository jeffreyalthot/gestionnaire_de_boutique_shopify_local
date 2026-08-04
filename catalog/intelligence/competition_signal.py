from __future__ import annotations


def competition_signal(similar_listing_count: int, median_review_count: float) -> float:
    pressure = min(1.0, similar_listing_count / 500) * 0.6 + min(1.0, median_review_count / 1000) * 0.4
    return max(0.0, min(1.0, pressure))
