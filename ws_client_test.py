import json

import aiohttp
import asyncio


# async def conn():
#     session = aiohttp.ClientSession()
#     async with session.ws_connect('http://127.0.0.1:8000/api/docker/37bb75c4-1ea3-4294-b2e4-4551a060a801/containers/ef/stats') as ws:
#         async for msg in ws:
#             print(msg.data)


async def conn():
    session = aiohttp.ClientSession()
    data = {'config': {
        "Image": "nginx:latest",
        "Env": {
            "env1": "value1",
            "env2": "value2",
            "env3": "value3",
        },
        "VolumesBind": [
            {
                "host_path": '/home/test1/',
                "container_path": "/mnt/vol1",
                "mode": 'ro',
            },
            {
                "host_path": '/home/test1/',
                "container_path": "/mnt/vol2",
                "mode": 'rw',
            }
        ],
        "PortsBind": [
            {
                'host_port': ['7070', '7072'],
                'container_port': '7070',
                'tcp': True,
                'udp': False
            },
            {
                'host_port': '7071',
                'container_port': '7071',
                'tcp': True,
                'udp': True
            }
        ],
    }}

    async with session.post(
            'http://127.0.0.1:8000/api/docker/37bb75c4-1ea3-4294-b2e4-4551a060a801/containers/run',
            json=data
    ) as resp:
        print(await resp.text())

asyncio.run(conn())

