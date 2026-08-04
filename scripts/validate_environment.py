import json
from app.bootstrap import bootstrap
from app.startup_checks import run_startup_checks
from config.paths import PROJECT_ROOT
if __name__=="__main__":
    app=bootstrap(); print(json.dumps(run_startup_checks(app.settings,app.container.db,PROJECT_ROOT),indent=2,default=str))
