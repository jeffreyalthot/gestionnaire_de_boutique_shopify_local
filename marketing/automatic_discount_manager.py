from __future__ import annotations
from dataclasses import asdict,dataclass
from marketing.discount_optimizer import DiscountOptimizer
from pricing.discount_margin_guard import DiscountMarginGuard

@dataclass(frozen=True,slots=True)
class AutomaticDiscountProposal:
    product_id: object
    requested_percent: float
    safe_maximum_percent: float
    applied_percent: float
    sale_price_cad: float
    safe: bool
    reasons: tuple[str,...]
    def as_dict(self):return asdict(self)

class AutomaticDiscountManager:
    def __init__(self) -> None:self.optimizer=DiscountOptimizer();self.guard=DiscountMarginGuard()
    def propose(self,product: dict[str,object],target_percent: float) -> dict[str,object]:return self.evaluate(product,target_percent).as_dict()
    def evaluate(self,product: dict[str,object],target_percent: float) -> AutomaticDiscountProposal:
        regular=float(product.get("price_cad",0));cost=float(product.get("landed_cost_cad",0));fees=float(product.get("fees_cad",0));safe=self.optimizer.maximum_safe_discount(regular_price_cad=regular,landed_cost_cad=cost,fees_cad=fees);requested=max(0,float(target_percent));applied=min(requested,safe);guard=self.guard.plan(regular_price_cad=regular,discount_percent=applied,landed_cost_cad=cost,fees_cad=fees);reasons=[]
        if requested>safe:reasons.append("capped_by_margin")
        if not guard.allowed:reasons.append("profit_floor")
        return AutomaticDiscountProposal(product.get("id"),requested,round(safe,2),round(applied,2),guard.sale_price_cad,bool(applied==requested and guard.allowed),tuple(reasons))
