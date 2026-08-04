from app.dependency_container import build_container

def test_2gb_profile_keeps_runtime_headroom(settings):
    container=build_container(settings); sample=container.resource_governor.sample()
    assert sample["budget"]["max_rss_mb"] <= 850 and sample["budget"]["worker_threads"] <= 2
