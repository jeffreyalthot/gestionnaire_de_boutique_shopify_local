from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import emit
from integrations.carriers.tracking_normalizer import normalize_tracking_number
def main():return emit({'input':'  ab-123  ','normalized':normalize_tracking_number('  ab-123  ')})
if __name__=='__main__':raise SystemExit(main())
