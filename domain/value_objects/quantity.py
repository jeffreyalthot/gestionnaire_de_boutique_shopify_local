from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Quantity:
    value: int
    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("La quantité ne peut pas être négative.")
