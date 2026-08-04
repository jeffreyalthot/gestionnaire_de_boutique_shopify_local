from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from math import isfinite
from typing import Any


def duration(seconds: float) -> str:
    try:
        total = max(0, int(float(seconds)))
    except (TypeError, ValueError):
        total = 0
    days, total = divmod(total, 86400)
    hours, total = divmod(total, 3600)
    minutes, total = divmod(total, 60)
    return f"{days:02d}j {hours:02d}h {minutes:02d}m {total:02d}s"


def money(value: Any, currency: str = "CAD") -> str:
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError):
        amount = Decimal("0.00")
    text = f"{amount:,.2f}".replace(",", " ")
    return f"{text} {str(currency).upper()}"


def percentage(value: Any, *, fraction: bool = True, precision: int = 1) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0
    if not isfinite(number):
        number = 0.0
    if fraction:
        number *= 100.0
    return f"{number:.{max(0, precision)}f} %"


def integer(value: Any) -> str:
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return "0"


def bytes_size(value: Any) -> str:
    try:
        size = max(0.0, float(value))
    except (TypeError, ValueError):
        size = 0.0
    units = ("o", "Kio", "Mio", "Gio", "Tio")
    index = 0
    while size >= 1024.0 and index < len(units) - 1:
        size /= 1024.0
        index += 1
    return f"{size:.1f} {units[index]}"


def timestamp(value: Any) -> str:
    if isinstance(value, datetime):
        moment = value
    elif value:
        try:
            moment = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return str(value)
    else:
        moment = datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def truncate(value: Any, width: int, *, marker: str = "...") -> str:
    text = str(value).replace("\r", " ").replace("\n", " ")
    width = max(0, int(width))
    if len(text) <= width:
        return text.ljust(width)
    if width <= len(marker):
        return marker[:width]
    return text[: width - len(marker)] + marker
