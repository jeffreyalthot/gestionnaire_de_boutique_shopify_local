from security.secret_scanner import scan_tree


def test_secret_scanner_ignores_build_artifacts(tmp_path):
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "artifact.log").write_text("4111 " + "1111 " + "1111 " + "1111", encoding="utf-8")
    (tmp_path / "source.py").write_text("value = 'safe'", encoding="utf-8")
    assert scan_tree(tmp_path) == []


def test_secret_scanner_still_scans_source(tmp_path):
    (tmp_path / "source.txt").write_text("shpat_" + "abcdefghijklmnopqrstuvwxyz123456", encoding="utf-8")
    assert scan_tree(tmp_path)[0][1] == "shopify_token"

def test_secret_scanner_ignores_named_build_variants(tmp_path):
    for name in ("build-2.2", "build_windows", "dist-release"):
        folder = tmp_path / name
        folder.mkdir()
        (folder / "artifact.log").write_text("4111 " + "1111 " + "1111 " + "1111", encoding="utf-8")
    assert scan_tree(tmp_path) == []
