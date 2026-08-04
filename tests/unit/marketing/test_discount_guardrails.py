from marketing.discount_guardrails import DiscountGuardrails

def test_discount_guardrail_preserves_minimum_margin():
    guard=DiscountGuardrails()
    assert guard.evaluate(100,50,10,30).allowed
    assert not guard.evaluate(100,80,30,30).allowed
