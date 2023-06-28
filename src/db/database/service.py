from db.database.database import async_session_maker
from logger.logs import logger
from node_manager.crud.crud_platforms import add_new_platform
from db.storage_config import (DOCKER_PLATFORM_NAME, SWARM_PLATFORM_NAME, DOCKER_TYPE,
                               DOCKER_DESCRIPTION, SWARM_DESCRIPTION, SWARM_TYPE)
from node_manager.schemas.schemas_platforms import PlatformCreate


async def init_models():
    try:
        async with async_session_maker() as session:
            db_data = {
                'docker': {
                    'name': DOCKER_PLATFORM_NAME,
                    'description': DOCKER_DESCRIPTION,
                    'type': DOCKER_TYPE
                },
                'swarm': {
                    'name': SWARM_PLATFORM_NAME,
                    'description': SWARM_DESCRIPTION,
                    'type': SWARM_TYPE
                }
            }
            for v in db_data.values():
                await add_new_platform(
                    new_platform=PlatformCreate(
                        name=v['name'],
                        description=v['description'],
                        type=v['type']
                    ),
                    session=session
                )

        logger['info'].info(
            "Database models have been successfully initialized"
        )
    except Exception as exc:
        logger['error'].error(
            f"Error initializing database models:\n{repr(exc)}"
        )
