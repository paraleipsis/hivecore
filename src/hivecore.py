import asyncio
import logging

from fastapi import FastAPI
from node_manager.router import router as router_hivecore
# from docker.router import router as router_docker
from rssh_client.hivecore_rssh_client import rssh_client

app = FastAPI()

app.include_router(router_hivecore)


@app.get('/')
async def home():
    return 'home'


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, rssh_client.start)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')
    uvicorn.run("hivecore:app", host='0.0.0.0', port=8000, log_level="info")
