from fastapi import FastAPI
from node_manager import api


def init_routes(application: FastAPI):
    application.include_router(api.platforms.router)
    application.include_router(api.environments.router)
    application.include_router(api.nodes.router)
