from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_async_session
from node_manager.schemas import schemas_platforms
from modules.schemas.response_schemas import GenericResponseModel
from node_manager.services import service_platforms


router = APIRouter(
    prefix='/platforms',
    tags=['Platforms']
)


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_platforms.PlatformRead]]
)
async def get_all_platforms_request(session: AsyncSession = Depends(get_async_session)):
    return await service_platforms.get_all_platforms(
        session=session
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_platforms.PlatformCreate]
)
async def create_platform_request(
        new_platform: schemas_platforms.PlatformCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_platforms.create_platform(
        session=session,
        new_platform=new_platform
    )


@router.get(
    '/{platform_name}',
    response_model=GenericResponseModel[schemas_platforms.PlatformRead]
)
async def get_platform_request(
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_platforms.get_platform(
        session=session,
        platform_name=platform_name,
    )


@router.delete(
    '/{platform_name}',
    response_model=GenericResponseModel[bool]
)
async def delete_platform_request(
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_platforms.delete_platform(
        session=session,
        platform_name=platform_name
    )
