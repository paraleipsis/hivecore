import json

import aiohttp
import asyncio


async def ws():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://127.0.0.1:8000/api/docker/37bb75c4-1ea3-4294-b2e4-4551a060a801/system/df/ws') as ws:
        async for msg in ws:
            print(msg.data)


async def conn():
    session = aiohttp.ClientSession()
    # data = {'config': {
    #     "Image": "nginx:latest",
    #     "Env": {
    #         "env1": "value1",
    #         "env2": "value2",
    #         "env3": "value3",
    #     },
    #     "VolumesBind": [
    #         {
    #             "host_path": '/home/test1/',
    #             "container_path": "/mnt/vol1",
    #             "mode": 'ro',
    #         },
    #         {
    #             "host_path": '/home/test1/',
    #             "container_path": "/mnt/vol2",
    #             "mode": 'rw',
    #         }
    #     ],
    #     "PortsBind": [
    #         {
    #             'host_port': ['7070', '7072'],
    #             'container_port': '7070',
    #             'tcp': True,
    #             'udp': False
    #         },
    #         {
    #             'host_port': '7071',
    #             'container_port': '7071',
    #             'tcp': True,
    #             'udp': True
    #         }
    #     ],
    # }}

    dockerfile = '''
    # Shared Volume
    FROM busybox:buildroot-2014.02
    VOLUME /data
    CMD ["/bin/sh"]
    '''

    params = {'force': 'true'}
    async with session.get(
            'http://127.0.0.1:8000/api/docker/37bb75c4-1ea3-4294-b2e4-4551a060a801/system/df/json',
            # params=params
    ) as resp:
        print(await resp.text())

    # async with session.post(
    #         'http://127.0.0.1:8080/docker/images/pull',
    #         params=data,
    # ) as resp:
    #     print(await resp.text())

    # async with session.get(
    #         'http://127.0.0.1:8000/api/docker/37bb75c4-1ea3-4294-b2e4-4551a060a801/images/json',
    # ) as resp:
    #     print(await resp.text())

asyncio.run(ws())

