import asyncio,json
from app.bootstrap import bootstrap
async def run():
    app=bootstrap()
    try: return {"configured":app.settings.live_alibaba_ready,"suppliers":await app.container.alibaba.suppliers() if app.settings.live_alibaba_ready else None}
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2,default=str))
