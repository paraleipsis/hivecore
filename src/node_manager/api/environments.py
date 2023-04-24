from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from node_manager.schemas import schemas_environments
from schemas.response_schemas import GenericResponseModel
from node_manager.services import service_environments


router = APIRouter(
    prefix='/platforms/{platform_name}/environments',
    tags=['Environments']
)


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_environments.EnvironmentRead]]
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
    '/',
    response_model=GenericResponseModel[schemas_environments.EnvironmentCreate]
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


@router.get(
    '/{environment}',
    response_model=GenericResponseModel[schemas_environments.EnvironmentRead]
)
async def get_environment_request(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_environments.get_environment(
        session=session,
        platform_name=platform_name,
        environment=environment
    )


@router.delete(
    '/{environment}',
    response_model=GenericResponseModel[bool]
)
async def delete_environment_request(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_environments.delete_environment(
        session=session,
        platform_name=platform_name,
        environment=environment
    )
