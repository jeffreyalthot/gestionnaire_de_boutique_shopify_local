from __future__ import annotations
import logging
from typing import Any


class LogEventSink(logging.Handler):
    def __init__(self, event_bus: Any, level: int = logging.INFO) -> None:
        super().__init__(level); self.event_bus=event_bus

    def emit(self, record: logging.LogRecord) -> None:
        try: self.event_bus.publish(self.format(record), record.levelname)
        except Exception: self.handleError(record)
