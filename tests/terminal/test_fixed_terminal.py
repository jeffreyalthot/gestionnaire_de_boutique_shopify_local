from dashboard.differential_renderer import DifferentialRenderer
from dashboard.fixed_line_registry import FixedLineRegistry
from dashboard.log_ring_buffer import LogRingBuffer
from dashboard.live_dashboard import LiveDashboard


def test_fixed_line_registry_rejects_duplicate_rows():
    registry = FixedLineRegistry()
    registry.register("header", 1)
    try:
        registry.register("other", 1)
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate row accepted")


def test_differential_renderer_only_changes_modified_lines():
    renderer = DifferentialRenderer()
    assert len(renderer.diff({1: "a", 2: "b"}, 10)) == 2
    patches = renderer.diff({1: "a", 2: "c"}, 10)
    assert len(patches) == 1 and patches[0].row == 2


def test_event_ring_has_fixed_capacity():
    ring = LogRingBuffer(2)
    ring.append("one")
    ring.append("two")
    ring.append("three")
    assert len(ring.lines()) == 2
    assert "three" in ring.lines()[-1]


def test_dashboard_always_renders_fixed_number_of_rows(settings):
    from app.dependency_container import build_container
    container = build_container(settings)
    dashboard = LiveDashboard(container)
    lines = dashboard.render_lines(100)
    assert len(lines) == dashboard.LINE_COUNT
    assert all(len(line) == 94 for line in lines)
