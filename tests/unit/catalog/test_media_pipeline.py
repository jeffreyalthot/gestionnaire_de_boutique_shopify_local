from pathlib import Path

import pytest

from catalog.media.content_type_detector import detect_content_type
from catalog.media.image_dimension_validator import validate_dimensions
from catalog.media.media_cache import MediaCache
from catalog.media.media_rights_guard import MediaRightsGuard
from catalog.media.media_url_validator import MediaURLValidator
from integrations.shopify.bulk_jsonl_stream import iter_jsonl


def test_media_url_guard_blocks_private_networks():
    validator = MediaURLValidator()
    assert not validator.validate("http://127.0.0.1/image.jpg").allowed
    assert not validator.validate("file:///etc/passwd").allowed
    assert validator.validate("https://example.com/image.jpg").allowed


def test_media_allowlist_is_enforced():
    validator = MediaURLValidator({"alicdn.com"})
    assert validator.validate("https://img.alicdn.com/a.jpg").allowed
    assert not validator.validate("https://example.com/a.jpg").allowed


def test_content_type_uses_magic_bytes():
    assert detect_content_type(b"\xff\xd8\xffanything") == "image/jpeg"
    assert detect_content_type(b"RIFF0000WEBPdata") == "image/webp"
    assert detect_content_type(b"text") == "application/octet-stream"


def test_dimension_guard_rejects_extremes():
    assert validate_dimensions(1200, 1200).allowed
    assert not validate_dimensions(100, 100).allowed
    assert not validate_dimensions(10000, 100).allowed


def test_rights_guard_requires_evidence():
    guard = MediaRightsGuard()
    assert guard.evaluate({"license": "supplier_authorized"}).allowed
    assert not guard.evaluate({}).allowed


def test_media_cache_prunes_oldest(tmp_path: Path):
    for index in range(3):
        path = tmp_path / f"{index}.bin"
        path.write_bytes(b"x" * 10)
    cache = MediaCache(tmp_path, 15)
    assert cache.prune() == 2
    assert cache.size() <= 15


def test_jsonl_stream_is_incremental_and_validated():
    rows = list(iter_jsonl(['{"id":1}\n', '\n', '{"id":2}\n']))
    assert rows == [{"id": 1}, {"id": 2}]
    with pytest.raises(ValueError):
        list(iter_jsonl(['[1,2]\n']))
