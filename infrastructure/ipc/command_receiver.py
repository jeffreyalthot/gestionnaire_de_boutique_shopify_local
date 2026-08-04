from __future__ import annotations
from collections import deque
from infrastructure.ipc.message import IpcMessage
class CommandReceiver:
    def __init__(self,capacity: int=100)->None: self._messages=deque(maxlen=capacity)
    def accept(self,message: IpcMessage)->bool:
        if message.type!='command': return False
        self._messages.append(message); return True
    def drain(self,limit: int=32)->list[IpcMessage]:
        values=[]
        while self._messages and len(values)<limit: values.append(self._messages.popleft())
        return values
