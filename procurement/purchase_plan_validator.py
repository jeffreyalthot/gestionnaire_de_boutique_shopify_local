from dataclasses import dataclass
from procurement.purchase_plan import PurchasePlan


@dataclass(frozen=True, slots=True)
class PurchasePlanValidation:
    valid: bool
    issues: tuple[str,...]


class PurchasePlanValidator:
    def validate(self, plan: PurchasePlan, *, financial_limit_cad: float) -> PurchasePlanValidation:
        issues=[]
        if not plan.order_id: issues.append("missing_order_id")
        if not plan.intents: issues.append("no_intents")
        calculated=round(sum(float(getattr(i,"amount_cad",0)) for i in plan.intents),2)
        if abs(calculated-plan.total_cad)>0.01: issues.append("total_mismatch")
        if plan.total_cad>financial_limit_cad: issues.append("financial_limit_exceeded")
        if len({getattr(i,"supplier_id","") for i in plan.intents})!=plan.supplier_count: issues.append("supplier_count_mismatch")
        return PurchasePlanValidation(not issues,tuple(issues))
