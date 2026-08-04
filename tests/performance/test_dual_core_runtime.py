from config.settings import Settings
def test_threads_limited(): assert Settings().ai_worker_threads<=2
