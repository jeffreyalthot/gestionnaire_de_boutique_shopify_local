import asyncio,json
from app.bootstrap import bootstrap
from integrations.shopify.schema_introspection import introspect_type
async def run(name: str="Product"):
    app=bootstrap()
    try: return await introspect_type(app.container.shopify_transport,name)
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2,default=str))
