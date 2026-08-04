from __future__ import annotations
import json,shutil
from datetime import datetime,timezone
from pathlib import Path
from uuid import uuid4
class Quarantine:
    def __init__(self,directory: Path)->None: self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True)
    def move(self,path: Path,reason: str)->Path:
        path=Path(path); destination=self.directory/f'{uuid4().hex}-{path.name}'
        shutil.move(str(path),destination)
        destination.with_suffix(destination.suffix+'.json').write_text(json.dumps({'reason':reason,'source':str(path),'at':datetime.now(timezone.utc).isoformat()}),encoding='utf-8')
        return destination
