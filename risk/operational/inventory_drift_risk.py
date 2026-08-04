from risk.risk_score import RiskScore


class InventoryDriftRisk:
    def assess(self, *, drift_units: int, expected_units: int) -> RiskScore:
        ratio=abs(drift_units)/max(1,expected_units); return RiskScore.build(min(1,ratio*2),("inventory_drift",) if ratio>.05 else ())
