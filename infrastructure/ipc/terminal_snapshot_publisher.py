from __future__ import annotations
from pathlib import Path
from typing import Any
from infrastructure.filesystem.atomic_file import atomic_write_text
import json
class TerminalSnapshotPublisher:
    def __init__(self,path: Path)->None: self.path=Path(path)
    def publish(self,snapshot: dict[str,Any])->Path: return atomic_write_text(self.path,json.dumps(snapshot,ensure_ascii=True,separators=(',',':')))
