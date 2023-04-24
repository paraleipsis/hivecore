from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_platforms
from node_manager.crud import crud_platforms
from schemas.response_schemas import GenericResponseModel


async def get_all_platforms(
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_platforms.get_platforms(session=session)
    return GenericResponseModel(data=data, total=len(data))


async def get_platform(
        platform_name: str,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_platforms.get_platform_by_name(
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data, total=1)


async def create_platform(
        new_platform: schemas_platforms.PlatformCreate,
        session: AsyncSession
) -> GenericResponseModel:
    await crud_platforms.add_new_platform(new_platform=new_platform, session=session)
    return GenericResponseModel(data=new_platform)


async def delete_platform(
        platform_name: str,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_platforms.delete_platform_by_name(platform_name=platform_name, session=session)
    return GenericResponseModel(data=data)
