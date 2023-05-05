from fastapi import FastAPI, APIRouter
from docker.api import (containers, images)
from node_manager.api import (environments, nodes, platforms)


def init_routes(application: FastAPI) -> None:
    """Include routes in all apps to core router with prefix '/api'.

       :param application:
          The :class:`FastAPI` application.

    """

    router = APIRouter(
        prefix='/api',
    )

    # node_manager
    router.include_router(platforms.router)
    router.include_router(environments.router)
    router.include_router(nodes.router)

    # docker
    router.include_router(containers.router)
    router.include_router(images.router)

    # main
    application.include_router(router)

    return None
