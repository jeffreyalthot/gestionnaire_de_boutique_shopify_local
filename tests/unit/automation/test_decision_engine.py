from automation.decisions.decision_engine import DecisionEngine

def test_decision_engine_uses_weighted_normalized_signals():
    result=DecisionEngine().score({"margin":.9,"risk":.2,"demand":.8},{"margin":.5,"risk":-.2,"demand":.3},threshold=.5)
    assert 0<=result.score<=1 and result.accepted and result.confidence==1
