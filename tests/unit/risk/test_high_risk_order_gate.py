from risk.fraud.high_risk_order_gate import HighRiskOrderGate
from risk.risk_score import RiskScore

def test_high_risk_gate_blocks_critical_order():
    decision=HighRiskOrderGate().evaluate(RiskScore.build(.9,["fraud_velocity"]))
    assert not decision.allowed and decision.action=="block"
