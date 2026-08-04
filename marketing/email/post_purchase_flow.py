from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class PostPurchaseStep:
    template: str
    due: bool
    delay_days: int
    allowed: bool
    reason: str
    def as_dict(self):return asdict(self)

class PostPurchaseFlow:
    STEPS=((1,"care_instructions"),(7,"review_request"),(21,"cross_sell"),(60,"replenishment_check"))
    def next_message(self,days_since_delivery: int) -> str|None:
        due=self.plan(days_since_delivery);return due[0].template if due else None
    def plan(self,days_since_delivery: int,*,consent: bool=True,refunded: bool=False,open_ticket: bool=False) -> tuple[PostPurchaseStep,...]:
        days=max(0,int(days_since_delivery));result=[]
        for delay,template in self.STEPS:
            if days>=delay:
                allowed=consent and not refunded and not open_ticket;reason="allowed" if allowed else "no_consent" if not consent else "customer_issue_open"
                result.append(PostPurchaseStep(template,True,delay,allowed,reason))
        return tuple(reversed(result))
