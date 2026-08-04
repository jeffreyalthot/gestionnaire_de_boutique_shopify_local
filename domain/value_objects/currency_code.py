from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class CurrencyCode:
    value: str
    def __post_init__(self) -> None:
        v=self.value.upper()
        if len(v)!=3: raise ValueError("Code devise invalide.")
        object.__setattr__(self,"value",v)
