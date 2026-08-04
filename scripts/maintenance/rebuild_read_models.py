from __future__ import annotations
from config.settings import get_settings
from infrastructure.database.engine import Database

def main() -> int:
    db=Database(get_settings().database_path); db.initialize()
    counts=db.counts(); db.set_value('read_model:counts', counts)
    db.set_value('read_model:finance', db.financial_snapshot())
    print({'status':'rebuilt','counts':counts}); return 0
if __name__=='__main__': raise SystemExit(main())
