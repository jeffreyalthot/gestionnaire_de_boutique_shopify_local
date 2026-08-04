from dataclasses import dataclass,field


@dataclass(frozen=True, slots=True)
class StoreProfile:
    name: str
    domain: str
    currency: str="CAD"
    timezone: str="America/Montreal"
    locales: tuple[str,...]=("fr-CA","en-CA")
    metadata: dict[str,object]=field(default_factory=dict)
