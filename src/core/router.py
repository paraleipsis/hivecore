from fastapi import FastAPI, APIRouter
from docker.api import (containers, images, networks, volumes, plugins, system)
from node_manager.api import (clusters, nodes, platforms, node_auth)


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
    router.include_router(clusters.router)
    router.include_router(nodes.router)
    router.include_router(node_auth.router)

    # docker
    router.include_router(containers.router)
    router.include_router(images.router)
    router.include_router(networks.router)
    router.include_router(volumes.router)
    router.include_router(plugins.router)
    router.include_router(system.router)

    # main
    application.include_router(router)

    return None
