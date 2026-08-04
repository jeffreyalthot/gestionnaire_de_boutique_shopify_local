from __future__ import annotations
import json
from pathlib import Path
from typing import IO,Any,Iterator
class JsonlStreamReader:
    def __init__(self,max_line_bytes: int=8*1024*1024)->None:self.max_line_bytes=max_line_bytes
    def read(self,source: Path|IO[bytes])->Iterator[dict[str,Any]]:
        owns=not hasattr(source,'read');handle=open(source,'rb') if owns else source
        try:
            for raw in handle:
                if len(raw)>self.max_line_bytes:raise ValueError('Ligne JSONL trop volumineuse.')
                if raw.strip():yield json.loads(raw)
        finally:
            if owns:handle.close()
