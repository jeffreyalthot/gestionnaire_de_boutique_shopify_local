from __future__ import annotations
from datetime import datetime, timezone
from config.settings import get_settings
from infrastructure.database.engine import Database

def main() -> int:
    db=Database(get_settings().database_path); db.initialize()
    result=db.verify_audit_chain()
    if not result.get('ok'): print(result); return 2
    db.insert_audit('audit.rotation_checkpoint','maintenance',{'at':datetime.now(timezone.utc).isoformat()})
    print({'status':'checkpointed','verification':result}); return 0
if __name__=='__main__': raise SystemExit(main())
