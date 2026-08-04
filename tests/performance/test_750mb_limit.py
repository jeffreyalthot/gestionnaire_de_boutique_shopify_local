from config.settings import Settings
def test_memory_limit(): assert Settings().ai_max_ram_mb<=750
