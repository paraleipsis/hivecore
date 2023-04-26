from fastapi import FastAPI, APIRouter
from node_manager import api as node_manager_api
from docker import api as docker_api


def init_routes(application: FastAPI) -> None:
    """Include routes in all apps to core router with prefix '/api'.

       :param application:
          The :class:`FastAPI` application.

    """

    router = APIRouter(
        prefix='/api',
    )

    # node_manager
    router.include_router(node_manager_api.platforms.router)
    router.include_router(node_manager_api.environments.router)
    router.include_router(node_manager_api.nodes.router)

    # docker
    router.include_router(docker_api.containers.router)

    # main
    application.include_router(router)

    return None
