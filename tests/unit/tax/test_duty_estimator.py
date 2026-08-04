from tax.duty_estimator import DutyEstimator

def test_duty_estimator_uses_landed_tax_base():
    result=DutyEstimator().estimate(100,20,.1,.15,5)
    assert result.duty==10 and result.tax==19.5 and result.total==34.5
