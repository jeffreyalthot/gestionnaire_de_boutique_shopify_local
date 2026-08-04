from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderProfitSnapshot:
    revenue_cad: float
    product_cost_cad: float
    shipping_cad: float
    fees_cad: float
    tax_cad: float = 0.0

    @property
    def profit_cad(self) -> float:
        return round(self.revenue_cad-self.product_cost_cad-self.shipping_cad-self.fees_cad-self.tax_cad,2)

    @property
    def margin_percent(self) -> float:
        return round(self.profit_cad/max(0.01,self.revenue_cad)*100,2)
