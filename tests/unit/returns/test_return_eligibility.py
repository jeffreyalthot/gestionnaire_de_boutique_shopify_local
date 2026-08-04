from datetime import datetime,timedelta,timezone
from returns.return_eligibility import ReturnEligibility

def test_return_eligibility_honours_window_and_damage_exception():
    now=datetime.now(timezone.utc); evaluator=ReturnEligibility()
    assert not evaluator.evaluate(delivered_at=now-timedelta(days=60),requested_at=now,category="general").eligible
    assert evaluator.evaluate(delivered_at=now-timedelta(days=60),requested_at=now,category="general",damaged=True).eligible
