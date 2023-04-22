from typing import Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from node_manager.exc_handlers.exceptions import AlreadyExistException, NoSuchEnvironment
from node_manager.models import models_environments
from node_manager.schemas import schemas_environments
from node_manager.crud.crud_platforms import get_platform_by_name


async def add_new_environment(
        new_environment:
        schemas_environments.EnvironmentCreate,
        platform_name: str,
        session: AsyncSession
) -> bool | None:

    platform = await get_platform_by_name(platform_name=platform_name, session=session)
    query = insert(models_environments.Environment).values(**new_environment.dict(), platform_id=platform.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Environment with such name in {platform_name} platform already exist')

    await session.commit()
    return True


async def get_environment_by_id(
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    query_environments = select(
        models_environments.Environment
    ).where(
        models_environments.Environment.id == environment_id and
        models_environments.Environment.platform_id == platform.id,
    ).options(selectinload(models_environments.Environment.nodes))

    result_query_environments = await session.execute(query_environments)
    environment = result_query_environments.scalars().first()

    if not environment:
        raise NoSuchEnvironment(f'Environment with id {environment_id} does not '
                                f'exist in platform with name {platform_name}')

    return environment


async def delete_environment_by_id(
        environment_id: int,
        platform_name: str,
        session: AsyncSession
) -> bool:
    environment = await get_environment_by_id(
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )

    if not environment:
        raise NoSuchEnvironment(f'Environment with id {environment_id} does not '
                                f'exist in platform with name {platform_name}')

    await session.delete(environment)
    await session.commit()
    return True
