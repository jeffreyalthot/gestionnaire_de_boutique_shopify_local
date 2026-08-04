from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class StockStatusDecision:
    status: str
    publishable: bool
    reason: str

def evaluate_stock_status(stock: int, *, unpublish: bool = True, continue_selling: bool = False, supplier_available: bool = True) -> StockStatusDecision:
    quantity = int(stock)
    if quantity > 0:
        return StockStatusDecision("active", True, "Stock disponible.")
    if continue_selling and supplier_available:
        return StockStatusDecision("active", True, "Vente différée autorisée avec disponibilité fournisseur.")
    if unpublish:
        return StockStatusDecision("draft", False, "Rupture de stock: publication suspendue.")
    return StockStatusDecision("active", True, "Rupture conservée visible selon la politique.")
def product_status_for_stock(stock: int, unpublish: bool = True) -> str:
    return evaluate_stock_status(stock, unpublish=unpublish).status
