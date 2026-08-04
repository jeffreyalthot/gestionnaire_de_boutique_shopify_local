import asyncio
from app.bootstrap import bootstrap

async def main():
    app=bootstrap()
    try:
        print(await app.container.command_bus.dispatch("runtime.recover",{}))
        print(await app.container.command_bus.dispatch("automation.cycle",{}))
    finally: await app.container.close()
asyncio.run(main())
