import asyncio
async def run(action,concurrency: int=4,iterations: int=100):
    semaphore=asyncio.Semaphore(concurrency)
    async def one():
        async with semaphore: return await action()
    return await asyncio.gather(*(one() for _ in range(iterations)),return_exceptions=True)
