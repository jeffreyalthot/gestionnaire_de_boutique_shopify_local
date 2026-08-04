from __future__ import annotations
from typing import Any
SENSITIVE={'access_token','refresh_token','app_secret','payment_token','password','card_number'}
def redact(value: Any):
    if isinstance(value,dict):return {k:('***' if k.lower() in SENSITIVE else redact(v)) for k,v in value.items()}
    if isinstance(value,list):return [redact(v) for v in value]
    return value
class AlibabaRequestAudit:
    def __init__(self,db: Any)->None:self.db=db
    def record(self,method: str,parameters: dict,response: dict|None=None,status: str='completed')->None:self.db.insert_audit('alibaba.request','integration',{'method':method,'parameters':redact(parameters),'response':redact(response or {}),'status':status})
