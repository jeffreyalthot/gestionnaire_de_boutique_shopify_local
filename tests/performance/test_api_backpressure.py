from config.settings import Settings
def test_http_concurrency(): assert Settings().max_concurrent_http_requests<=4
