from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class TaxRegistrationDecision:
    required: bool
    annual_sales_cad: Decimal
    threshold_cad: Decimal
    remaining_before_threshold_cad: Decimal
    reason: str

def evaluate_tax_registration(annual_sales_cad: object, threshold_cad: object = 30000) -> TaxRegistrationDecision:
    sales = Decimal(str(annual_sales_cad)).quantize(Decimal("0.01"))
    threshold = Decimal(str(threshold_cad)).quantize(Decimal("0.01"))
    if sales < 0 or threshold <= 0:
        raise ValueError("Les ventes doivent être positives et le seuil supérieur à zéro.")
    required = sales >= threshold
    remaining = max(Decimal("0.00"), threshold - sales)
    return TaxRegistrationDecision(required, sales, threshold, remaining, "Seuil atteint." if required else "Seuil non atteint.")

def tax_registration_required(annual_sales_cad: float, threshold_cad: float = 30000) -> bool:
    return evaluate_tax_registration(annual_sales_cad, threshold_cad).required
