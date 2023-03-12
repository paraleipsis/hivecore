from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from database import get_async_session
from platform_manager import models, schemas
from sqlalchemy import insert, select


async def get_platforms(session: AsyncSession):
    query = select(models.Platform)
    data = await session.execute(query)
    return data.scalars().all()


async def get_platform_by_name(platform_name: str, session: AsyncSession):
    query = select(models.Platform).where(models.Platform.name == platform_name)
    result = await session.execute(query)
    data = result.scalars().first()

    return data


async def add_new_platform(new_platform: schemas.PlatformCreate, session: AsyncSession):
    query = insert(models.Platform).values(**new_platform.dict())
    await session.execute(query)
    await session.commit()

    return True
