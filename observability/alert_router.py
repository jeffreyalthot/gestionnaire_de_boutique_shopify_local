class AlertRouter:
    def route(self, severity: str) -> tuple[str,...]:
        if severity=="critical": return ("terminal","audit","operator")
        if severity in {"error","warning"}: return ("terminal","audit")
        return ("audit",)
