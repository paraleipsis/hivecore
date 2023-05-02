import aiohttp
import asyncio


async def conn():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://127.0.0.1:8000/api/docker/containers/37bb75c4-1ea3-4294-b2e4-4551a060a801/ws') as ws:
        async for msg in ws:
            print(msg.data)

asyncio.run(conn())
