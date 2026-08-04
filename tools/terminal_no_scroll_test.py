from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import emit
from dashboard.fixed_region_layout import FixedRegionLayout
def main():
 layout=FixedRegionLayout(30);layout.reserve('page',0,20);layout.reserve('events',20,7);layout.reserve('input',29,1);return emit({'line_count':layout.line_count,'regions':[r.__dict__ for r in layout.regions()]})
if __name__=='__main__':raise SystemExit(main())
