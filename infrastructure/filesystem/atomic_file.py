from __future__ import annotations
import os,tempfile
from pathlib import Path

def atomic_write_bytes(path: Path,data: bytes)->Path:
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise
    return path

def atomic_write_text(path: Path,text: str,encoding: str='utf-8')->Path: return atomic_write_bytes(path,text.encode(encoding))
