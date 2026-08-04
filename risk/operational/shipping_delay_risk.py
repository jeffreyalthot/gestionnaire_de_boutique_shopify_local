from risk.risk_score import RiskScore


class ShippingDelayRisk:
    def assess(self, *, overdue_days: float, carrier_reliability: float) -> RiskScore:
        return RiskScore.build(min(1,max(0,overdue_days)/14+(1-carrier_reliability)*.5),("shipping_delay",) if overdue_days>0 else ())
