from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TaxContext:
    origin_country: str
    destination_country: str
    destination_region: str=""
    category: str="general"
    amount_cad: float=0.0
