from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

import asyncio
from tools.runtime_tool import emit
from app.bootstrap import bootstrap
async def run():
 app=bootstrap();result=await app.run_once();await app.container.close();return result
def main():return emit(asyncio.run(run()))
if __name__=='__main__':raise SystemExit(main())
