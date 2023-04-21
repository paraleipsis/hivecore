from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_async_session
from node_manager.schemas import schemas_platforms
from core.schemas import core_schemas
from node_manager.services import service_platforms
from node_manager.api.router import router


@router.get(
    '/',
    response_model=core_schemas.GenericResponseModel[List[schemas_platforms.PlatformsListRead]]
)
async def get_all_platforms_request(session: AsyncSession = Depends(get_async_session)):
    return await service_platforms.get_all_platforms(
        session=session
    )


@router.post(
    '/',
    response_model=core_schemas.GenericResponseModel[schemas_platforms.PlatformCreate]
)
async def create_platform_request(
        new_platform: schemas_platforms.PlatformCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_platforms.create_platform(
        session=session,
        new_platform=new_platform
    )


@router.delete(
    '/{platform_name}',
    response_model=core_schemas.GenericResponseModel[bool]
)
async def delete_platform_request(
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_platforms.delete_platform(
        session=session,
        platform_name=platform_name
    )
