from __future__ import annotations
class JobBudget:
    def __init__(self,max_running: int=1,max_heavy: int=1)->None: self.max_running=max(1,min(max_running,2)); self.max_heavy=max(0,min(max_heavy,1)); self.running=0; self.heavy=0
    def acquire(self,heavy: bool=False)->bool:
        if self.running>=self.max_running or heavy and self.heavy>=self.max_heavy: return False
        self.running+=1; self.heavy+=int(heavy); return True
    def release(self,heavy: bool=False)->None: self.running=max(0,self.running-1); self.heavy=max(0,self.heavy-int(heavy))
