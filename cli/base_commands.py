from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from typing import Any
@dataclass(frozen=True,slots=True)
class CommandResult:
    command:str;ok:bool;data:Any;message:str="";generated_at:str=""
    def to_dict(self):
        out=asdict(self);out["generated_at"]=self.generated_at or datetime.now(timezone.utc).isoformat();return out
class BaseCommands:
    resource="runtime"
    def __init__(self,container) -> None:self.container=container
    def result(self,command: str,data: Any,ok: bool=True,message: str="") -> dict[str,Any]:return CommandResult(f"{self.resource}.{command}",ok,data,message).to_dict()
    def execute(self,action: str="status",**options: Any) -> dict[str,Any]:
        method=getattr(self,f"action_{action}",None)
        if method is None:return self.result(action,{},False,f"action inconnue: {action}")
        return method(**options)
    def action_status(self,**_: Any) -> dict[str,Any]:return self.result("status",self.container.status())
