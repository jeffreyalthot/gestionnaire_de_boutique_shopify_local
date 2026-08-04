from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class Percentage:
    value: Decimal

    def __post_init__(self) -> None:
        value = Decimal(str(self.value))
        if value < 0 or value > 100:
            raise ValueError("Un pourcentage doit être compris entre 0 et 100.")
        object.__setattr__(self, "value", value)

    @property
    def ratio(self) -> Decimal:
        return self.value / Decimal("100")
