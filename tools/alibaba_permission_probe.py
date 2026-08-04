import asyncio,json
from app.bootstrap import bootstrap
from integrations.alibaba.permission_probe import AlibabaPermissionProbe
async def run():
    app=bootstrap()
    try: return await AlibabaPermissionProbe(app.container.alibaba_gateway).probe_read_capabilities() if app.settings.live_alibaba_ready else {"configured":False}
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2))
