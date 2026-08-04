from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from tools.runtime_tool import database,emit
from automation.reconciliation.order_reconciler import OrderReconciler
def main():
 _,db=database();return emit({'checkpoint_rows':db.query('SELECT * FROM reconciliation_checkpoints ORDER BY updated_at DESC LIMIT 20'),'orders':db.scalar('SELECT COUNT(*) FROM orders',default=0)})
if __name__=='__main__':raise SystemExit(main())
