import logging
def force_log_flush() -> None:
    for handler in logging.getLogger().handlers:
        handler.flush()
