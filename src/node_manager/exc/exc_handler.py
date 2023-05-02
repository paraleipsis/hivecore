from fastapi import FastAPI

from modules.exc.exceptions.exceptions_nodes import NoSuchNode
from node_manager.exc.exceptions import (NoSuchPlatform, AlreadyExistException, NoSuchEnvironment)
from node_manager.exc.handlers.handlers_environments import environment_not_exists_exception_handler
from node_manager.exc.handlers.handlers_global import (global_exception_handler,
                                                       connection_refused_exception_handler,
                                                       already_exist_exception_handler)
from node_manager.exc.handlers.handlers_nodes import node_not_exists_exception_handler
from node_manager.exc.handlers.handlers_platforms import platform_not_exists_exception_handler


def init_exc_handlers(application: FastAPI) -> None:
    # globals
    application.add_exception_handler(Exception, global_exception_handler)
    application.add_exception_handler(ConnectionRefusedError, connection_refused_exception_handler)
    application.add_exception_handler(AlreadyExistException, already_exist_exception_handler)

    # platforms
    application.add_exception_handler(NoSuchPlatform, platform_not_exists_exception_handler)

    # environments
    application.add_exception_handler(NoSuchEnvironment, environment_not_exists_exception_handler)

    # nodes
    application.add_exception_handler(NoSuchNode, node_not_exists_exception_handler)
