from risk.risk_score import RiskScore


class ApiOutageRisk:
    def assess(self, *, failures: int, window_calls: int, outage_minutes: float) -> RiskScore:
        rate=failures/max(1,window_calls); return RiskScore.build(min(1,rate*.8+outage_minutes/120),("api_instability",) if rate>.2 else ())
