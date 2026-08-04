from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from infrastructure.database.integrity_checker import IntegrityChecker
def main():
 _,db=database();r=IntegrityChecker(db).run();return emit(r.as_dict(),0 if r.ok else 2)
if __name__=='__main__':raise SystemExit(main())
