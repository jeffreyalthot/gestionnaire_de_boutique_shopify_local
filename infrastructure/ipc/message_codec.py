from __future__ import annotations
import json
from infrastructure.ipc.message import IpcMessage
class MessageCodec:
    @staticmethod
    def encode(message: IpcMessage)->bytes:
        payload=json.dumps(message.as_dict(),ensure_ascii=True,separators=(',',':')).encode('utf-8')
        if len(payload)>1048576: raise ValueError('Message IPC trop volumineux.')
        return len(payload).to_bytes(4,'big')+payload
    @staticmethod
    def decode(data: bytes)->IpcMessage:
        if len(data)<4: raise ValueError('Trame IPC incomplète.')
        length=int.from_bytes(data[:4],'big')
        if length>1048576 or len(data[4:])!=length: raise ValueError('Longueur IPC invalide.')
        value=json.loads(data[4:]); return IpcMessage(value['type'],value['payload'],value['id'],value['created_at'])
