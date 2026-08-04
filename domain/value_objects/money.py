from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from config.constants import MONEY_QUANTUM

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = "CAD"

    def __post_init__(self) -> None:
        object.__setattr__(self, "amount", Decimal(str(self.amount)).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP))
        if len(self.currency) != 3:
            raise ValueError("Le code de devise doit contenir trois caractères.")

    def __add__(self, other: "Money") -> "Money":
        self._same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: Decimal | float | int) -> "Money":
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def _same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Les devises doivent être identiques.")

    def as_float(self) -> float:
        return float(self.amount)

    def as_dict(self) -> dict[str, str]:
        return {"amount": str(self.amount), "currency": self.currency}
