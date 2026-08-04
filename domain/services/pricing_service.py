from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal

from pricing.pricing_engine import PriceDecision, PricingEngine

__all__ = ["PricingEngine", "PriceDecision", "price_quote"]


def price_quote(engine: PricingEngine, product_cost_cad: Decimal, shipping_cost_cad: Decimal) -> dict[str, object]:
    decision = engine.calculate(Decimal(str(product_cost_cad)), Decimal(str(shipping_cost_cad)))
    result = asdict(decision)
    result["sale_price_cad"] = str(decision.sale_price_cad)
    result["landed_cost_cad"] = str(decision.landed_cost_cad)
    result["margin_percent"] = str(decision.margin_percent)
    result["breakdown"] = {key: str(value) for key, value in asdict(decision.breakdown).items()}
    return result
