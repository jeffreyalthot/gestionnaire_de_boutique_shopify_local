import asyncio,json
from app.bootstrap import bootstrap
async def run() -> dict[str,object]:
    app=bootstrap()
    try: return {"configured":app.settings.live_shopify_ready,"shop":await app.container.shopify.shop() if app.settings.live_shopify_ready else None}
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2,default=str))
