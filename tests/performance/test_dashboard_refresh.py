from config.settings import Settings
def test_dashboard_default(): assert Settings().dashboard_refresh_seconds==5
