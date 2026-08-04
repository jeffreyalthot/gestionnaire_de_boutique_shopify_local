from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
def main():
 _,db=database();result=db.verify_audit_chain();return emit(result,0 if result.get('ok') else 2)
if __name__=='__main__':raise SystemExit(main())
