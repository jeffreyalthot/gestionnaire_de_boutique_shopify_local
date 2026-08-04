from __future__ import annotations
import json
import logging
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from config.paths import LOG_DIR

_SECRET_KEYS = ("token", "secret", "password", "authorization", "cvv", "card_number", "pin")

def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: ("***" if any(s in k.lower() for s in _SECRET_KEYS) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "context"):
            payload["context"] = redact(getattr(record, "context"))
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)

def configure_logging(level: str = "INFO") -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))
    file_handler = RotatingFileHandler(LOG_DIR / "orchestrator.jsonl", maxBytes=20_000_000, backupCount=10, encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())
    root.addHandler(console)
    root.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
