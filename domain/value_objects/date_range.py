from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class DateRange:
    start: datetime
    end: datetime
    def __post_init__(self) -> None:
        if self.end < self.start: raise ValueError("Plage de dates invalide.")
