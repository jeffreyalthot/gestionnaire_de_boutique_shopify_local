class PermissionMinimizer:
    def minimize(self, required: set[str], requested: set[str], allowed: set[str]) -> tuple[set[str],set[str]]:
        granted=requested & allowed; missing=required-granted
        return granted,missing
