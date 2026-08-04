from dataclasses import dataclass,field


@dataclass(frozen=True, slots=True)
class SupplierCandidate:
    supplier_id: str
    name: str
    country_code: str
    years_active: float=0.0
    trade_assurance: bool=False
    verified: bool=False
    capabilities: tuple[str,...]=field(default_factory=tuple)
    metadata: dict[str,object]=field(default_factory=dict)
