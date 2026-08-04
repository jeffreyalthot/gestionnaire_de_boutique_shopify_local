from dashboard.differential_renderer import DifferentialRenderer

def test_resize_reformats_existing_rows_without_adding_rows():
    renderer=DifferentialRenderer(); first=renderer.diff({1:"abcdefghijk"},12); second=renderer.diff({1:"abcdefghijk"},6)
    assert len(first)==len(second)==1 and len(second[0].text)==6
