from __future__ import annotations
from dataclasses import asdict,dataclass
@dataclass
class JobHealth:
    name: str; successes: int=0; failures: int=0; consecutive_failures: int=0; last_error: str=''
    def success(self): self.successes+=1; self.consecutive_failures=0; self.last_error=''
    def failure(self,error: str): self.failures+=1; self.consecutive_failures+=1; self.last_error=error[:1000]
    def as_dict(self): return asdict(self)
