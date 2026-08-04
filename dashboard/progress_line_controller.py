class ProgressLineController:
    def __init__(self, width: int = 30) -> None:
        self.width = max(10, width)

    def render(self, current: int, total: int, label: str = '') -> str:
        total = max(0, total); current = max(0, min(current, total))
        ratio = current / total if total else 0.0
        filled = round(self.width * ratio)
        return f"{label} [{'#' * filled}{'-' * (self.width - filled)}] {current}/{total} {ratio * 100:5.1f}%"
