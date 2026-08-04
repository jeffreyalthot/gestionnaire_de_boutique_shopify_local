from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SKU:
    value: str
    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise ValueError("Le SKU est obligatoire.")
        object.__setattr__(self, "value", normalized)
