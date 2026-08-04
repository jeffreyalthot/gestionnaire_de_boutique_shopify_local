from observability.action_trace import ActionTrace


class WorkflowTrace:
    def __init__(self, name: str) -> None: self.name=name; self.actions: list[ActionTrace]=[]
    def start(self, action: str, **attributes) -> ActionTrace:
        trace=ActionTrace(action,attributes=attributes); self.actions.append(trace); return trace
    def snapshot(self) -> dict[str,object]: return {"workflow":self.name,"actions":[{"name":x.name,"status":x.status,"attributes":x.attributes} for x in self.actions]}
