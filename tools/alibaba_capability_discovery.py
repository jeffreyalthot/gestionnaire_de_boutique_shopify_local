from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from integrations.alibaba.api_profile import AlibabaApiProfile
from integrations.alibaba.api_profile_registry import AlibabaApiProfileRegistry
def main():
 s,db=database();r=AlibabaApiProfileRegistry();r.register(AlibabaApiProfile('configured',frozenset({'read.products','read.orders'}),frozenset(),s.live_payment_ready));return emit({'profiles':r.names(),'live_ready':s.live_alibaba_ready,'payment_ready':s.live_payment_ready})
if __name__=='__main__':raise SystemExit(main())
