import asyncio,json
from app.bootstrap import bootstrap
from workflows.alibaba_reconciliation_workflow import AlibabaReconciliationWorkflow
async def run():
    app=bootstrap()
    try:
        result={"shopify":"skipped","alibaba":"skipped"}
        if app.settings.live_alibaba_ready: result["alibaba"]=await AlibabaReconciliationWorkflow(app.container.alibaba).execute()
        return result
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2,default=str))
