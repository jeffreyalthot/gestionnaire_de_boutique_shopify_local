from app.dependency_container import build_container


def test_runtime_budget_fits_2gb_machine(settings):
    container = build_container(settings)
    sample = container.resource_governor.sample()
    assert sample["budget"]["max_rss_mb"] <= 850
    assert sample["budget"]["worker_threads"] <= 2
    assert sample["budget"]["max_http_concurrency"] <= 2
    assert sample["within_memory_budget"]
