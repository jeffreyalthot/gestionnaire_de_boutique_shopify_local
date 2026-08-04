from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class JourneyDecision:
    stage: str
    next_action: str
    priority: str
    automation_allowed: bool
    reason: str
    def as_dict(self):return asdict(self)

class CustomerJourney:
    def stage(self,*,orders: int,days_since_order: int,abandoned_checkout: bool=False) -> str:return self.evaluate(orders=orders,days_since_order=days_since_order,abandoned_checkout=abandoned_checkout).stage
    def evaluate(self,*,orders: int,days_since_order: int,abandoned_checkout: bool=False,consent: bool=True,open_ticket: bool=False,chargebacks: int=0) -> JourneyDecision:
        if abandoned_checkout:stage,action,priority="abandoned_checkout","recover_checkout","high"
        elif orders<=0:stage,action,priority="prospect","educate","normal"
        elif days_since_order<=14:stage,action,priority="post_purchase","support_and_review","normal"
        elif days_since_order>=120:stage,action,priority="winback","winback_offer","medium"
        else:stage,action,priority="retention","cross_sell","normal"
        allowed=consent and not open_ticket and chargebacks==0;reason="allowed" if allowed else "no_consent" if not consent else "customer_issue_open" if open_ticket else "financial_risk"
        return JourneyDecision(stage,action,priority,allowed,reason)
