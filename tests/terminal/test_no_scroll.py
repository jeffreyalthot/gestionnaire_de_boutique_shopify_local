from dashboard.fixed_region_layout import FixedRegionLayout

def test_all_terminal_regions_fit_without_scrolling():
    layout=FixedRegionLayout(30)
    layout.reserve("page",0,20); layout.reserve("events",20,7); layout.reserve("input",29,1)
    assert max(region.end for region in layout.regions())==29
