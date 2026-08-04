from automation.policies.policy_engine import ActionPolicy,PolicyEngine

def test_financial_policy_requires_approval_and_limit():
    policy=ActionPolicy("pay",risk="financial",max_amount_cad=50)
    engine=PolicyEngine(dry_run=False)
    assert engine.evaluate(policy,amount_cad=25).reason=="explicit_approval_required"
    assert engine.evaluate(policy,amount_cad=75,approved=True).reason=="financial_limit_exceeded"
