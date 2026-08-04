class QueueRegistry:
    def __init__(self)->None: self._queues={}
    def register(self,name: str,priority: int=100)->None:
        if not name or name in self._queues: raise ValueError('File invalide ou déjà enregistrée.')
        self._queues[name]=priority
    def ordered(self)->tuple[str,...]: return tuple(name for name,_ in sorted(self._queues.items(),key=lambda item:(item[1],item[0])))
