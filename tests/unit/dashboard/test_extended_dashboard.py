import pytest

from dashboard.fixed_region_layout import FixedRegionLayout
from dashboard.input_line_controller import InputLineController
from dashboard.progress_line_controller import ProgressLineController
from dashboard.terminal_event_bus import TerminalEventBus


def test_fixed_regions_cannot_overlap():
    layout = FixedRegionLayout(30)
    layout.reserve('header', 0, 3)
    with pytest.raises(ValueError):
        layout.reserve('body', 2, 10)


def test_input_controller_never_adds_lines():
    controller = InputLineController(max_length=8)
    controller.insert('abc\ndefghijkl')
    assert '\n' not in controller.render(20)
    assert controller.submit() == 'abcdefgh'


def test_progress_is_bounded():
    text = ProgressLineController(10).render(20, 10, 'X')
    assert '10/10' in text and '100.0%' in text


def test_event_bus_is_ring_buffer():
    bus = TerminalEventBus(2)
    bus.publish('a'); bus.publish('b'); bus.publish('c')
    assert [item.message for item in bus.latest(10)] == ['b', 'c']
