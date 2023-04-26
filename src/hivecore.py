from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.startup_tasks.create_channel import create_pubsub_channels
from node_manager.exc.exc_handler import init_exc_handlers as node_manager_init_exc_handlers
from core.startup_tasks.run_rssh import run_rssh_client
from core.router import init_routes
from core import middleware
from core.config import PUBSUB_CHANNELS


async def test():
    from modules.pubsub.pubsub import pb
    from modules.pubsub.subscriber import Subscriber

    sub = Subscriber(pubsub=pb, channel='connections')

    while True:
        msg = await sub.get()
        print(msg)


def run_test():
    import asyncio
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(coro=test(), loop=loop)


def pre_startup(application: FastAPI) -> None:
    node_manager_init_exc_handlers(application=application)
    init_routes(application=application)


async def startup() -> None:
    create_pubsub_channels(PUBSUB_CHANNELS)
    run_rssh_client()
    run_test()


async def shutdown() -> None:
    pass


def create_app() -> FastAPI:
    application = FastAPI(
        title='Hivecore',
        docs_url='/api/docs',
        openapi_url='/api/openapi.json',
        middleware=middleware.utils,
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    pre_startup(application)

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hivecore:app", host='0.0.0.0', port=8000, log_level="info")
