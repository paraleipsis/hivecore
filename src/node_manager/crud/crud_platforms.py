from typing import Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from node_manager.exc_handlers.exceptions import NoSuchPlatform, AlreadyExistException
from node_manager.models import models_platforms
from node_manager.schemas import schemas_platforms


async def get_platforms(
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(models_platforms.Platform).options(selectinload(models_platforms.Platform.environments))
    result = await session.execute(query)
    data = result.scalars().all()
    return data


async def get_platform_by_name(
        platform_name: str,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(
        models_platforms.Platform
    ).where(
        models_platforms.Platform.name == platform_name
    ).options(selectinload(models_platforms.Platform.environments))
    result = await session.execute(query)
    data = result.scalars().first()

    if data is None:
        raise NoSuchPlatform(f'Platform {platform_name} does not exist')

    return data


async def add_new_platform(
        new_platform: schemas_platforms.PlatformCreate,
        session: AsyncSession
) -> bool:
    query = insert(models_platforms.Platform).values(**new_platform.dict())

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Platform with such name already exist')

    await session.commit()
    return True


async def delete_platform_by_name(
        platform_name: str,
        session: AsyncSession
) -> bool:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    if not platform:
        raise NoSuchPlatform(f'Platform {platform_name} does not exist')

    await session.delete(platform)
    await session.commit()
    return True
