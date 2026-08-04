from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta


@dataclass(frozen=True, slots=True)
class DeliveryEstimate:
    earliest: date
    latest: date
    confidence: float
    business_days: bool = True

    def as_dict(self):
        data = asdict(self); data["earliest"] = self.earliest.isoformat(); data["latest"] = self.latest.isoformat(); return data


class DeliveryEstimator:
    def estimate(self, ship_date: date, *, minimum_days: int, maximum_days: int,
                 handling_days: int = 0, confidence: float = 0.8) -> DeliveryEstimate:
        if minimum_days < 0 or maximum_days < minimum_days:
            raise ValueError("Fenêtre de livraison invalide.")
        def add_business_days(start: date, days: int) -> date:
            current=start; remaining=days
            while remaining:
                current += timedelta(days=1)
                if current.weekday() < 5: remaining -= 1
            return current
        start = add_business_days(ship_date, handling_days + minimum_days)
        end = add_business_days(ship_date, handling_days + maximum_days)
        return DeliveryEstimate(start, end, max(0.0, min(1.0, confidence)))
