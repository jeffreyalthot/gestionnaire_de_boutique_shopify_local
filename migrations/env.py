from infrastructure.database.engine import Database
from config.settings import get_settings
def run_migrations() -> None: Database(get_settings().database_path).initialize()
