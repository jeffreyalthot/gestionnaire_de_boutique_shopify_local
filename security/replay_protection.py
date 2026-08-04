from datetime import datetime, timezone
def timestamp_within_window(timestamp: datetime, seconds: int = 300) -> bool:
    now = datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return abs((now - timestamp).total_seconds()) <= seconds
