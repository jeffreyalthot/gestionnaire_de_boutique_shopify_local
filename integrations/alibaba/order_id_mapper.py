from __future__ import annotations
from typing import Any
class AlibabaOrderIdMapper:
    def __init__(self,db: Any)->None:self.db=db
    def save(self,local_order_id: str,supplier_order_id: str)->None:self.db.set_value(f'alibaba:order-map:{local_order_id}',supplier_order_id)
    def supplier_id(self,local_order_id: str)->str:return str(self.db.get_value(f'alibaba:order-map:{local_order_id}',''))
