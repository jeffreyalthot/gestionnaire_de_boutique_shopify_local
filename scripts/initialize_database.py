from app.bootstrap import bootstrap
if __name__=="__main__":
    app=bootstrap(); app.container.db.initialize(); print(app.container.db.health())
