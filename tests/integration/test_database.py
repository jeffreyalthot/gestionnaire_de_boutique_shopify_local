def test_database_health(db): assert db.health()["ok"]
