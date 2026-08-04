import json
from app.bootstrap import bootstrap
def run(): 
    app=bootstrap(); return {"health":app.container.db.health(),"counts":app.container.db.counts(),"finance":app.container.db.financial_snapshot()}
if __name__=="__main__": print(json.dumps(run(),indent=2))
