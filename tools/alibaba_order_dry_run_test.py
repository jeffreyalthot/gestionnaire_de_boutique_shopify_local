from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

import asyncio
from tools.runtime_tool import emit
from workflows.order_to_supplier_workflow import OrderToSupplierWorkflow
async def run():return (await OrderToSupplierWorkflow().execute({'order_id':'dry-1','paid':True},dry_run=True,approved=True)).as_dict()
def main():return emit(asyncio.run(run()))
if __name__=='__main__':raise SystemExit(main())
