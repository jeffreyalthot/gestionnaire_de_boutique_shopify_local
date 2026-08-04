import asyncio
async def refresh_loop(action,seconds: float,stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        await action()
        try: await asyncio.wait_for(stop_event.wait(),timeout=seconds)
        except asyncio.TimeoutError: continue
