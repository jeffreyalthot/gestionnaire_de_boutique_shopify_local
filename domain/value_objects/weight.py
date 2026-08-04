from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Weight:
    kilograms: float
    def __post_init__(self) -> None:
        if self.kilograms < 0: raise ValueError("Poids invalide.")
