from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PurchasePlan:
    order_id: str
    intents: tuple[object,...]=field(default_factory=tuple)
    total_cad: float=0.0
    supplier_count: int=0
