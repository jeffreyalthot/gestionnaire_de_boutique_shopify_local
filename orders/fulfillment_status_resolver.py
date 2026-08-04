class FulfillmentStatusResolver:
    def resolve(self, *, total_lines: int, fulfilled_lines: int, cancelled_lines: int = 0) -> str:
        active = max(0, total_lines - cancelled_lines)
        if active == 0: return "cancelled"
        if fulfilled_lines <= 0: return "unfulfilled"
        if fulfilled_lines < active: return "partially_fulfilled"
        return "fulfilled"
