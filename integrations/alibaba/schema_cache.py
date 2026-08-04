from __future__ import annotations
import json,time
from pathlib import Path
from typing import Any
class SchemaCache:
    def __init__(self,directory: Path,ttl_seconds: int=86400)->None:self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True);self.ttl=ttl_seconds
    def put(self,name: str,value: dict[str,Any])->Path:
        path=self.directory/f'{name}.json';path.write_text(json.dumps({'cached_at':time.time(),'value':value},separators=(',',':')),encoding='utf-8');return path
    def get(self,name: str)->dict[str,Any]|None:
        path=self.directory/f'{name}.json'
        if not path.exists():return None
        item=json.loads(path.read_text(encoding='utf-8'))
        return item['value'] if time.time()-float(item['cached_at'])<=self.ttl else None
