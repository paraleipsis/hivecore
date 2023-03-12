from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from platform_manager import models, schemas
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.orm import selectinload


async def get_platforms(session: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    query = select(models.Platform).options(selectinload(models.Platform.environments))
    result = await session.execute(query)
    data = result.scalars().all()
    return data


async def get_platform_by_name(platform_name: str, session: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    query = select(
        models.Platform
    ).where(
        models.Platform.name == platform_name
    ).options(selectinload(models.Platform.environments))
    result = await session.execute(query)
    data = result.scalars().first()
    return data


async def add_new_platform(new_platform: schemas.PlatformCreate, session: AsyncSession) -> bool:
    query = insert(models.Platform).values(**new_platform.dict())
    await session.execute(query)
    await session.commit()
    return True


async def delete_platform_by_name(platform_name: str, session: AsyncSession) -> bool:
    query = select(
        models.Platform
    ).where(
        models.Platform.name == platform_name
    ).options(selectinload(models.Platform.environments))
    result = await session.execute(query)
    data = result.scalars().first()
    if not data:
        return False
    await session.delete(data)
    await session.commit()
    return True
