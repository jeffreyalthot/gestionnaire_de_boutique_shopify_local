from __future__ import annotations
from typing import Any
class SampleRepository:
    def __init__(self,db: Any)->None:self.db=db
    def put(self,identifier: str,value: dict)->None:self.db.set_value('alibaba:sample'+':'+identifier,value)
    def get(self,identifier: str,default=None):return self.db.get_value('alibaba:sample'+':'+identifier,default)
