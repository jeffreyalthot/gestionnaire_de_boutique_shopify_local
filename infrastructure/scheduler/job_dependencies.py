from __future__ import annotations
class JobDependencies:
    def __init__(self)->None: self._deps={}
    def add(self,job: str,*dependencies: str)->None: self._deps[job]=tuple(dict.fromkeys(dependencies))
    def ready(self,job: str,completed: set[str])->bool: return all(item in completed for item in self._deps.get(job,()))
    def validate(self)->None:
        def visit(node,trail):
            if node in trail: raise ValueError('Cycle de dépendances scheduler.')
            for dep in self._deps.get(node,()): visit(dep,trail|{node})
        for node in self._deps: visit(node,set())
