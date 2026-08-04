from infrastructure.database.integrity_checker import IntegrityChecker

def test_database_remains_healthy_after_transactions(db):
    for index in range(20): db.set_value(f"lock-test:{index}",index)
    report=IntegrityChecker(db).run()
    assert report.ok and report.quick_check=="ok"
