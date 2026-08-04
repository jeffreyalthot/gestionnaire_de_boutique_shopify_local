from __future__ import annotations

from datetime import date, timedelta


class PayoutSchedule:
    def next_business_day(self, start: date, delay_days: int = 2) -> date:
        current = start
        remaining = max(0, delay_days)
        while remaining:
            current += timedelta(days=1)
            if current.weekday() < 5:
                remaining -= 1
        return current
