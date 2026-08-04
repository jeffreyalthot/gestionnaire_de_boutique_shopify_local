from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class RiskContext:
    entity_type: str
    entity_id: str
    amount_cad: float=0.0
    country_code: str=""
    customer_id: str=""
    supplier_id: str=""
    attributes: dict[str,object]=field(default_factory=dict)
