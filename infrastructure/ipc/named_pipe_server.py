from __future__ import annotations
class NamedPipeServer:
    def __init__(self,path: str,max_bytes: int=1048580)->None: self.path=path; self.max_bytes=max_bytes
    def receive(self)->bytes:
        with open(self.path,'rb',buffering=0) as pipe:
            data=pipe.read(self.max_bytes+1)
        if len(data)>self.max_bytes: raise ValueError('Message pipe trop volumineux.')
        return data
