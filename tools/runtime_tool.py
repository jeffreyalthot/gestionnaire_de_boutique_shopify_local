from __future__ import annotations
import json
from config.settings import get_settings
from infrastructure.database.engine import Database

def database():
    settings=get_settings();db=Database(settings.database_path);db.initialize();return settings,db
def emit(value,code=0):
    print(json.dumps(value,ensure_ascii=False,indent=2,default=str));return code
