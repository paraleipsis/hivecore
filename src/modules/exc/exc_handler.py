from fastapi import FastAPI

from modules.exc.exceptions.exceptions_nodes import (NoSuchNode, PlatformNodeLinkError, NodeSnapshotError)
from modules.exc.exceptions.exceptions import (AlreadyExistException)
from modules.exc.exceptions.exceptions_platforms import (NoSuchPlatform)
from modules.exc.exceptions.exceptions_clusters import (NoSuchCluster)
from modules.exc.exceptions.exceptions_docker import (NoSuchDockerObject, DockerSnapshotDoesNotExist)
from modules.exc.handlers.handlers_clusters import cluster_not_exists_exception_handler
from modules.exc.handlers.handlers_global import (global_exception_handler,
                                                  connection_refused_exception_handler,
                                                  already_exist_exception_handler)
from modules.exc.handlers.handlers_nodes import node_not_exists_exception_handler, platform_node_link_exception_handler, \
    platform_node_snapshot_exception_handler
from modules.exc.handlers.handlers_platforms import platform_not_exists_exception_handler
from modules.exc.handlers.handlers_docker import (docker_object_not_exists_exception_handler,
                                                  docker_snapshot_not_exists_exception_handler)


def init_exc_handlers(application: FastAPI) -> None:
    # globals
    application.add_exception_handler(Exception, global_exception_handler)
    application.add_exception_handler(ConnectionRefusedError, connection_refused_exception_handler)
    application.add_exception_handler(AlreadyExistException, already_exist_exception_handler)

    # platforms
    application.add_exception_handler(NoSuchPlatform, platform_not_exists_exception_handler)

    # environments
    application.add_exception_handler(NoSuchCluster, cluster_not_exists_exception_handler)

    # nodes
    application.add_exception_handler(NoSuchNode, node_not_exists_exception_handler)
    application.add_exception_handler(PlatformNodeLinkError, platform_node_link_exception_handler)
    application.add_exception_handler(NodeSnapshotError, platform_node_snapshot_exception_handler)

    # docker
    application.add_exception_handler(NoSuchDockerObject, docker_object_not_exists_exception_handler)
    application.add_exception_handler(DockerSnapshotDoesNotExist, docker_snapshot_not_exists_exception_handler)
