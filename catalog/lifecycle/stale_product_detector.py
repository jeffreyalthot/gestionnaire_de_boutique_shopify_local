from datetime import datetime, timedelta, timezone


def stale(updated_at: datetime, days: int = 30, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return now - updated_at >= timedelta(days=days)
