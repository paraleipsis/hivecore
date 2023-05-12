from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.startup_tasks.create_channel import create_pubsub_channels
from modules.exc.exc_handler import init_exc_handlers
from core.startup_tasks.run_rssh import run_rssh_client
from core.router import init_routes
from core import middleware
from config.server_config import PUBSUB_CHANNELS, HOST, PORT, LOG_LEVEL, DOCS_URL, OPENAPI_URL
from db.broker.broker import run_kafka_producer
from core.startup_tasks.run_node_monitor import run_node_monitor, get_node_monitor
from db.broker.broker import get_kafka_producer
from rssh_client.rssh import init_rssh_client
from rssh_client.rssh import get_rssh_client


def pre_startup(application: FastAPI) -> None:
    init_exc_handlers(application=application)
    init_routes(application=application)


async def startup() -> None:
    create_pubsub_channels(PUBSUB_CHANNELS)
    init_rssh_client()
    run_rssh_client()
    await run_kafka_producer()
    run_node_monitor()


async def shutdown() -> None:
    node_monitor = get_node_monitor()
    await node_monitor.stop_monitor()

    rssh_client = get_rssh_client()
    await rssh_client.stop_listener()

    kafka_producer = get_kafka_producer()
    await kafka_producer.stop()


def create_app() -> FastAPI:
    application = FastAPI(
        title='Hivecore',
        docs_url=DOCS_URL,
        openapi_url=OPENAPI_URL,
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

    uvicorn.run(
        "hivecore:app",
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL
    )
