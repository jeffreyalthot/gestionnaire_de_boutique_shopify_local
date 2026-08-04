from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import emit
def main():
 staged={'resource':'IMAGE','filename':'dry-run.jpg','mimeType':'image/jpeg','httpMethod':'POST'};return emit({'dry_run':True,'staged_input':staged,'network_called':False})
if __name__=='__main__':raise SystemExit(main())
