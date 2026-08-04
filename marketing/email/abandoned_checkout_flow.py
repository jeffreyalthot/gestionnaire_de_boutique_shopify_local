from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class CheckoutMessage:
    template: str
    due_after_minutes: int
    due: bool
    allowed: bool
    reason: str
    incentive_percent: float
    def as_dict(self):return asdict(self)

class AbandonedCheckoutFlow:
    STEPS=((30,"reminder_1",0.),(1440,"reminder_2",5.),(4320,"final_reminder",8.))
    def schedule(self,age_minutes: int) -> tuple[str,...]:return tuple(step.template for step in self.plan(age_minutes) if step.due and step.allowed)
    def plan(self,age_minutes: int,*,consent: bool=True,converted: bool=False,open_support_ticket: bool=False,maximum_discount_percent: float=10) -> tuple[CheckoutMessage,...]:
        age=max(0,int(age_minutes));result=[]
        for delay,template,incentive in self.STEPS:
            due=age>=delay;allowed=consent and not converted and not open_support_ticket;reason="allowed" if allowed else "no_consent" if not consent else "already_converted" if converted else "support_issue_open"
            result.append(CheckoutMessage(template,delay,due,allowed,reason,min(incentive,max(0,maximum_discount_percent))))
        return tuple(result)
