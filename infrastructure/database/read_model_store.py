from __future__ import annotations
from typing import Any
class ReadModelStore:
    def __init__(self,db: Any,prefix: str='read_model')->None: self.db=db; self.prefix=prefix
    def put(self,name: str,value: Any)->None: self.db.set_value(f'{self.prefix}:{name}',value)
    def get(self,name: str,default: Any=None)->Any: return self.db.get_value(f'{self.prefix}:{name}',default)
    def delete(self,name: str)->int: return self.db.execute('DELETE FROM key_values WHERE key=?',(f'{self.prefix}:{name}',))
