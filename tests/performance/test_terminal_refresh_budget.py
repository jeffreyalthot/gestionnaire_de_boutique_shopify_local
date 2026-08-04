from time import perf_counter
from app.dependency_container import build_container
from dashboard.live_dashboard import LiveDashboard

def test_terminal_refresh_remains_lightweight(settings):
    container=build_container(settings); dashboard=LiveDashboard(container,.5)
    start=perf_counter()
    for _ in range(100): dashboard.render_lines(100)
    assert perf_counter()-start < 3.0
