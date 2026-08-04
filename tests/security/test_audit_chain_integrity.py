def test_audit_chain_detects_no_tampering(db):
    db.insert_audit("test.one","tester",{"value":1}); db.insert_audit("test.two","tester",{"value":2})
    report=db.verify_audit_chain()
    assert report["ok"] and report["entries"]>=2
