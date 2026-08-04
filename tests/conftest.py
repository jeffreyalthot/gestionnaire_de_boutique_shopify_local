import os
from pathlib import Path
import pytest
from config.settings import Settings
from infrastructure.database.engine import Database
@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(app_env="test",app_dry_run=True,app_database_path=tmp_path/"test.db",
                    master_encryption_key="test-key",ai_max_ram_mb=750)
@pytest.fixture
def db(settings: Settings) -> Database:
    database=Database(settings.database_path); database.initialize(); return database
