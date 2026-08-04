from suppliers.due_diligence import DueDiligence

def test_due_diligence_rejects_unverified_supplier():
    result=DueDiligence().evaluate({"verified_business":False,"years_active":0,"dispute_rate":.2,"trade_assurance":False})
    assert not result.accepted and "business_not_verified" in result.reasons
