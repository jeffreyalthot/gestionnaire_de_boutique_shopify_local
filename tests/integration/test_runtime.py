from app.dependency_container import build_container
def test_container(settings):
    c=build_container(settings)
    assert c.status()["runtime"]["dry_run"]
