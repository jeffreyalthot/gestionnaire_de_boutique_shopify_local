from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ExternalId:
    platform: str
    value: str
    def __post_init__(self) -> None:
        if not self.platform or not self.value: raise ValueError("Identifiant externe incomplet.")
