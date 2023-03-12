from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from platform_manager import models, schemas
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.orm import selectinload

from sqlalchemy.exc import IntegrityError

from platform_manager.exceptions import NoSuchPlatform, AlreadyExistException, NoSuchEnvironment, NoSuchNode


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

    if data is None:
        raise NoSuchPlatform

    return data


async def add_new_platform(new_platform: schemas.PlatformCreate, session: AsyncSession) -> bool:
    query = insert(models.Platform).values(**new_platform.dict())

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException

    await session.commit()
    return True


async def delete_platform_by_name(platform_name: str, session: AsyncSession) -> bool:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    await session.delete(platform)
    await session.commit()
    return True


async def add_new_environment(new_environment: schemas.EnvironmentCreate,
                              platform_name: str, session: AsyncSession) -> bool | None:

    platform = await get_platform_by_name(platform_name=platform_name, session=session)
    query = insert(models.Environment).values(**new_environment.dict(), platform_id=platform.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException

    await session.commit()
    return True


async def get_environment_by_id(platform_name: str, environment_id: int,
                                session: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    query_environments = select(
        models.Environment
    ).where(
        models.Environment.id == environment_id and
        models.Environment.platform_id == platform.id,
    ).options(selectinload(models.Environment.nodes))

    result_query_environments = await session.execute(query_environments)
    environment = result_query_environments.scalars().first()

    if not environment:
        raise NoSuchEnvironment

    return environment


async def delete_environment_by_id(environment_id: int, platform_name: str, session: AsyncSession) -> bool:
    environment = await get_environment_by_id(
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )

    if not environment:
        raise NoSuchEnvironment

    await session.delete(environment)
    await session.commit()
    return True


async def get_node_by_id(node_id: int, platform_name: str, environment_id: int,
                         session: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    environment = await get_environment_by_id(
        platform_name=platform_name,
        environment_id=environment_id,
        session=session
    )

    query_nodes = select(
        models.Node
    ).where(
        models.Node.id == node_id and
        models.Node.environment_id == environment.id,
    )

    result_query_nodes = await session.execute(query_nodes)
    node = result_query_nodes.scalars().first()

    if not node:
        raise NoSuchNode

    return node


async def add_new_node(new_node: schemas.NodeCreate, platform_name: str,
                       environment_id: int, session: AsyncSession) -> bool | None:

    environment = await get_environment_by_id(
        platform_name=platform_name,
        environment_id=environment_id,
        session=session
    )
    query = insert(models.Node).values(**new_node.dict(), environment_id=environment.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException

    await session.commit()
    return True


async def delete_node_by_id(node_id: int, environment_id: int, platform_name: str, session: AsyncSession) -> bool:
    node = await get_node_by_id(
        node_id=node_id,
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )

    if not node:
        raise NoSuchNode

    await session.delete(node)
    await session.commit()
    return True


