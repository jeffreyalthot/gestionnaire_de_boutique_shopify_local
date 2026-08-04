from config.settings import get_settings
from config.paths import ensure_runtime_directories
from observability.logger import configure_logging
from app.application import Application
def bootstrap() -> Application:
    settings=get_settings(); ensure_runtime_directories(); configure_logging(settings.app_log_level)
    return Application(settings)
