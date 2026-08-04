from risk.risk_score import RiskScore


class RefundExposure:
    def assess(self, *, refundable_revenue_cad: float, cash_cad: float, historical_refund_rate: float) -> RiskScore:
        ratio=refundable_revenue_cad/max(.01,cash_cad); return RiskScore.build(min(1,ratio*.5+historical_refund_rate*2),("refund_liability",) if ratio>.5 else ())
