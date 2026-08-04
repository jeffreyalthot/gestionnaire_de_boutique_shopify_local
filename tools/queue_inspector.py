import json
from app.bootstrap import bootstrap
def run():
    app=bootstrap(); return {"stats":app.container.queue.stats(),"dead":app.container.db.query("SELECT * FROM tasks WHERE status='dead' LIMIT 100")}
if __name__=="__main__": print(json.dumps(run(),indent=2,default=str))
