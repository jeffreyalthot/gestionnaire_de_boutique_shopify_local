from __future__ import annotations
import inspect,shlex
from typing import Any,Callable
class CommandRouter:
    def __init__(self) -> None:self.handlers={};self.aliases={}
    def register(self,name: str,handler: Callable[...,Any],aliases: tuple[str,...]=()) -> None:
        key=name.strip().lower()
        if not key or key in self.handlers:raise ValueError("commande invalide ou dupliquée")
        self.handlers[key]=handler
        for alias in aliases:
            alias=alias.strip().lower()
            if alias in self.handlers or alias in self.aliases:raise ValueError("alias dupliqué")
            self.aliases[alias]=key
    def names(self) -> tuple[str,...]:return tuple(sorted(self.handlers))
    def parse(self,line: str) -> tuple[str,dict[str,object]]:
        tokens=shlex.split(line)
        if not tokens:raise ValueError("commande vide")
        name=tokens[0].lower();options={}
        for token in tokens[1:]:
            if "=" in token:key,value=token.split("=",1);options[key.lstrip("-").replace("-","_")]=value
            else:options.setdefault("args",[]).append(token)
        return self.aliases.get(name,name),options
    async def execute(self,name: str,*args,**kwargs):
        key=self.aliases.get(name.strip().lower(),name.strip().lower())
        if key not in self.handlers:raise KeyError(key)
        result=self.handlers[key](*args,**kwargs);return await result if inspect.isawaitable(result) else result
    async def execute_line(self,line: str):
        name,options=self.parse(line);return await self.execute(name,**options)
