from __future__ import annotations
from dataclasses import dataclass
from math import ceil

@dataclass(frozen=True, slots=True)
class SafetyStockDecision:
    supplier_stock: int
    safety_stock: int
    reserved: int
    available: int
    reorder_point: int
    reorder_quantity: int

def calculate_safety_stock(*, average_daily_sales: float, lead_time_days: float, variability_factor: float = 0.25, minimum: int = 0) -> int:
    if average_daily_sales < 0 or lead_time_days < 0 or variability_factor < 0:
        raise ValueError("Les paramètres de stock de sécurité ne peuvent pas être négatifs.")
    expected = average_daily_sales * lead_time_days
    return max(int(minimum), ceil(expected * variability_factor))

def inventory_decision(supplier_stock: int, safety_quantity: int, reserved: int = 0, *, average_daily_sales: float = 0, lead_time_days: float = 0, target_cover_days: float = 30) -> SafetyStockDecision:
    stock, safety, held = max(0, int(supplier_stock)), max(0, int(safety_quantity)), max(0, int(reserved))
    available = max(0, stock - safety - held)
    reorder_point = ceil(max(0.0, average_daily_sales) * max(0.0, lead_time_days)) + safety
    target = ceil(max(0.0, average_daily_sales) * max(0.0, target_cover_days)) + safety
    reorder_quantity = max(0, target - max(0, stock - held)) if stock - held <= reorder_point else 0
    return SafetyStockDecision(stock, safety, held, available, reorder_point, reorder_quantity)

def available_for_sale(supplier_stock: int, safety_quantity: int, reserved: int = 0) -> int:
    return inventory_decision(supplier_stock, safety_quantity, reserved).available
