from catalog.media.media_url_validator import MediaURLValidator

def test_media_guard_blocks_local_and_non_https_sources():
    guard=MediaURLValidator()
    assert not guard.validate("http://127.0.0.1/x.jpg").allowed
    assert not guard.validate("file:///tmp/x.jpg").allowed
    assert guard.validate("https://example.com/x.jpg").allowed
