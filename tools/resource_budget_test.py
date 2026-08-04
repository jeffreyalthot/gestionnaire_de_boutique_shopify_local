from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from infrastructure.process.memory_limit import MemoryLimit
def main():
 s,_=database();snapshot=MemoryLimit(s.runtime_max_rss_mb).snapshot();return emit(snapshot,0 if snapshot['ok'] else 2)
if __name__=='__main__':raise SystemExit(main())
