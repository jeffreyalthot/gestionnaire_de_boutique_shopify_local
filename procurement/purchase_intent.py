from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PurchaseIntent:
    id: str
    idempotency_key: str
    order_id: str
    supplier_id: str
    amount_cad: float
    currency: str="CAD"
    lines: tuple[dict[str,object],...]=field(default_factory=tuple)
    status: str="planned"
