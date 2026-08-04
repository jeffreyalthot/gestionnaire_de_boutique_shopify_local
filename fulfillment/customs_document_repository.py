from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


class CustomsDocumentRepository:
    def __init__(self, root: Path, db: Any) -> None:
        self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True); self.db=db

    def store(self, order_id: str, source: Path) -> dict[str,str|int]:
        data=source.read_bytes(); digest=hashlib.sha256(data).hexdigest(); destination=self.root/f"{order_id}-{digest[:16]}{source.suffix.lower()}"
        destination.write_bytes(data); self.db.set_value(f"customs-doc:{order_id}:{digest}",{"path":str(destination),"sha256":digest})
        return {"path":str(destination),"sha256":digest,"byte_size":len(data)}
