from __future__ import annotations
from pathlib import Path
class NamedPipeClient:
    def __init__(self,path: str)->None: self.path=path
    def send(self,data: bytes)->int:
        with open(self.path,'wb',buffering=0) as pipe: return pipe.write(data)
