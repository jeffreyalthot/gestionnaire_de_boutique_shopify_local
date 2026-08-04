from app.resource_governor import ResourceGovernor,RuntimeBudget

def test_dual_core_profile_never_requests_excess_workers():
    governor=ResourceGovernor(RuntimeBudget(worker_threads=2,max_http_concurrency=2,max_rss_mb=850))
    sample=governor.sample()
    assert sample["budget"]["worker_threads"]<=2 and sample["budget"]["max_http_concurrency"]<=2
