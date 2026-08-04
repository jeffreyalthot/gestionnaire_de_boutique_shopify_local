class MethodAliasRegistry:
    def __init__(self,aliases: dict[str,str]|None=None)->None:self.aliases=dict(aliases or {})
    def register(self,canonical: str,*aliases: str)->None:
        self.aliases[canonical]=canonical
        for alias in aliases:self.aliases[alias]=canonical
    def resolve(self,name: str)->str:return self.aliases.get(name,name)
