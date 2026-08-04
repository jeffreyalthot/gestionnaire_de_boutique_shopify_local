from __future__ import annotations
from infrastructure.ipc.message import IpcMessage
from infrastructure.ipc.message_codec import MessageCodec
class RuntimeBridge:
    def __init__(self,transport)->None: self.transport=transport
    def send(self,message_type: str,payload: dict)->int: return self.transport.send(MessageCodec.encode(IpcMessage(message_type,payload)))
