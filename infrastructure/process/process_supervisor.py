from __future__ import annotations
import subprocess
from dataclasses import dataclass
from typing import Sequence
@dataclass
class ManagedProcess:
    name: str; command: Sequence[str]; process: subprocess.Popen|None=None
class ProcessSupervisor:
    def __init__(self)->None: self.processes={}
    def register(self,name: str,command: Sequence[str])->None:
        if name in self.processes: raise ValueError('Processus déjà enregistré.')
        self.processes[name]=ManagedProcess(name,tuple(command))
    def start(self,name: str)->int:
        item=self.processes[name]
        if item.process and item.process.poll() is None: return item.process.pid
        item.process=subprocess.Popen(item.command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); return item.process.pid
    def stop_all(self)->None:
        for item in self.processes.values():
            if item.process and item.process.poll() is None: item.process.terminate()
