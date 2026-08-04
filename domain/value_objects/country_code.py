from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class CountryCode:
    value: str
    def __post_init__(self) -> None:
        v=self.value.upper()
        if len(v)!=2: raise ValueError("Code pays invalide.")
        object.__setattr__(self,"value",v)
