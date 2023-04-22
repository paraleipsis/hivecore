from fastapi import FastAPI

from node_manager.exc_handlers.exc_handler import init_exc_handlers as node_manager_init_exc_handlers
from startup_tasks.run_rssh import run_rssh_client
from router import init_routes


def pre_startup(application: FastAPI) -> None:
    node_manager_init_exc_handlers(application=application)
    init_routes(application=application)


async def startup() -> None:
    run_rssh_client()


async def shutdown() -> None:
    pass


def create_app() -> FastAPI:
    application = FastAPI(
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    pre_startup(application)

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("hivecore:app", host='0.0.0.0', port=8000, log_level="info")
