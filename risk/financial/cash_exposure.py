from risk.risk_score import RiskScore


class CashExposure:
    def assess(self, *, committed_cad: float, available_cad: float, reserve_cad: float) -> RiskScore:
        usable=max(.01,available_cad-reserve_cad); ratio=max(0,committed_cad)/usable
        return RiskScore.build(min(1,ratio), ("cash_reserve_pressure",) if ratio>=.5 else ())
