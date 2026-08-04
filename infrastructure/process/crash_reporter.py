from __future__ import annotations
import json,traceback
from datetime import datetime,timezone
from pathlib import Path
from infrastructure.filesystem.atomic_file import atomic_write_text
class CrashReporter:
    def __init__(self,directory: Path)->None: self.directory=Path(directory)
    def write(self,exc: BaseException,context: dict|None=None)->Path:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); path=self.directory/f'crash-{stamp}.json'
        return atomic_write_text(path,json.dumps({'at':stamp,'type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc(),'context':context or {}},ensure_ascii=False,indent=2))
