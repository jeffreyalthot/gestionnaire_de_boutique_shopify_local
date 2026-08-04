from risk.risk_score import RiskScore


class SupplierFailureRisk:
    def assess(self, *, cancellation_rate: float, late_rate: float, dispute_rate: float) -> RiskScore:
        score=cancellation_rate*.4+late_rate*.35+dispute_rate*.5
        return RiskScore.build(min(1,score),("supplier_reliability",) if score>.25 else ())
