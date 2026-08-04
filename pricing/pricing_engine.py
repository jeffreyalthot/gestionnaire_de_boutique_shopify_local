from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from config.settings import Settings
from pricing.gross_margin_calculator import sale_price_for_margin,gross_margin_percent
from pricing.markup_calculator import sale_price_for_markup
from pricing.psychological_pricing import psychological_price
from pricing.landed_cost_calculator import LandedCostCalculator,LandedCostBreakdown

@dataclass(frozen=True,slots=True)
class PriceDecision:
    sale_price_cad: Decimal
    landed_cost_cad: Decimal
    margin_percent: Decimal
    breakdown: LandedCostBreakdown

class PricingEngine:
    def __init__(self,settings: Settings) -> None:
        self.settings=settings; self.landed=LandedCostCalculator()
    def calculate(self,product_cost_cad: Decimal,shipping_cost_cad: Decimal) -> PriceDecision:
        breakdown=self.landed.calculate(product_cost_cad,shipping_cost_cad,
            Decimal(str(self.settings.platform_fee_percent)),
            Decimal(str(self.settings.duty_tax_buffer_percent)),
            Decimal(str(self.settings.currency_buffer_percent)),
            Decimal(str(self.settings.refund_reserve_percent)))
        if self.settings.pricing_mode=="gross_margin":
            price=sale_price_for_margin(breakdown.total,Decimal(str(self.settings.target_gross_margin_percent)))
        else:
            price=sale_price_for_markup(breakdown.total,Decimal(str(self.settings.target_gross_margin_percent)))
        if self.settings.price_rounding_mode=="psychological":
            price=psychological_price(price,Decimal(str(self.settings.price_rounding_ending)))
        else:
            price=price.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        margin=gross_margin_percent(price,breakdown.total)
        if margin<Decimal(str(self.settings.minimum_gross_margin_percent)):
            raise ValueError(f"Marge calculée insuffisante: {margin:.2f} %")
        return PriceDecision(price,breakdown.total,margin,breakdown)
