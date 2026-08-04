from catalog.media.media_rights_guard import MediaRightsGuard

def test_media_rights_require_explicit_evidence():
    guard=MediaRightsGuard()
    assert guard.evaluate({"license":"supplier_authorized"}).allowed
    assert not guard.evaluate({"explicitly_forbidden":True}).allowed
