class TerminalMetricsSink:
    def __init__(self, state: dict[str,object]) -> None: self.state=state
    def write(self, metric: str, value: float) -> None: self.state.setdefault("metrics",{})[metric]=value
