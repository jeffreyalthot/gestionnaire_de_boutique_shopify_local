def interval_from_expression(expression: str) -> int:
    mapping={"@hourly":3600,"@daily":86400,"@weekly":604800}
    if expression in mapping: return mapping[expression]
    if expression.startswith("*/") and expression.endswith(" * * * *"):
        return int(expression[2:].split()[0])*60
    raise ValueError("Expression cron non prise en charge.")
