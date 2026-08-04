import json
from app.bootstrap import bootstrap
def run():
    app=bootstrap(); return app.container.ai.status()
if __name__=="__main__": print(json.dumps(run(),indent=2))
