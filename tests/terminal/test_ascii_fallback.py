from dashboard.differential_renderer import DifferentialRenderer

def test_control_characters_are_sanitized():
    patch=DifferentialRenderer().diff({1:"ok\x01value"},20)[0]
    assert "\x01" not in patch.text and "?" in patch.text
