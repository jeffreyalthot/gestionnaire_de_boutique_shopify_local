from observability.logger import get_logger

def log_event(logger_name: str, level: str, message: str, **context: object) -> None:
    logger = get_logger(logger_name)
    getattr(logger, level.lower(), logger.info)(message, extra={"context": context})
