from pricing.discount_margin_guard import DiscountMarginGuard


class DiscountOptimizer:
    def maximum_safe_discount(self,*,regular_price_cad: float,landed_cost_cad: float,fees_cad: float=0,step: float=.5) -> float:
        guard=DiscountMarginGuard(); candidate=0.; best=0.
        while candidate<=80:
            if guard.evaluate(regular_price_cad=regular_price_cad,discount_percent=candidate,landed_cost_cad=landed_cost_cad,fees_cad=fees_cad).allowed: best=candidate
            else: break
            candidate+=max(.1,step)
        return round(best,2)
