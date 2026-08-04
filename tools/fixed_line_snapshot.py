from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from config.settings import get_settings
from app.dependency_container import build_container
from dashboard.live_dashboard import LiveDashboard
def main():
 c=build_container(get_settings());lines=LiveDashboard(c,.5).render_lines(100);return emit({'line_count':len(lines),'unique_lengths':sorted(set(map(len,lines))),'lines':lines})
if __name__=='__main__':raise SystemExit(main())
