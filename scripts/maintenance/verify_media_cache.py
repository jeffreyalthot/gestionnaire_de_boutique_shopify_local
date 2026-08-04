from __future__ import annotations
import hashlib
from pathlib import Path
from config.settings import get_settings
from infrastructure.database.engine import Database

def main() -> int:
    db=Database(get_settings().database_path); db.initialize(); errors=[]; checked=0
    for row in db.query("SELECT id,local_path,sha256 FROM media_assets WHERE local_path<>''"):
        path=Path(row['local_path']); checked+=1
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']: errors.append(row['id'])
    print({'checked':checked,'invalid':errors}); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
