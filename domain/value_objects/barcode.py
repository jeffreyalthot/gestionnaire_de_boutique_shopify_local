from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Barcode:
    value: str
    def __post_init__(self) -> None:
        if self.value and not self.value.replace("-", "").isalnum():
            raise ValueError("Code-barres invalide.")
