from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from node_manager.schemas import schemas_environments, schemas_platforms
from core.schemas import core_schemas
from node_manager.services import service_environments
from node_manager.api.router import router


@router.get(
    '/{platform_name}',
    response_model=core_schemas.GenericResponseModel[schemas_platforms.PlatformDetailsRead]
)
async def get_all_environments_request(
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_environments.get_all_environments(
        session=session,
        platform_name=platform_name
    )


@router.post(
    '/{platform_name}',
    response_model=core_schemas.GenericResponseModel[schemas_environments.EnvironmentCreate]
)
async def create_environment_request(
        platform_name: str,
        new_environment: schemas_environments.EnvironmentCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_environments.create_environment(
        session=session,
        platform_name=platform_name,
        new_environment=new_environment
    )


@router.delete(
    '/{platform_name}/{environment_id}',
    response_model=core_schemas.GenericResponseModel[bool]
)
async def delete_environment_request(
        platform_name: str,
        environment_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_environments.delete_environment(
        session=session,
        platform_name=platform_name,
        environment_id=environment_id
    )
