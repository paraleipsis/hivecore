from typing import Any, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.exc import IntegrityError

from node_manager.utils import title_to_lowercase, is_uuid
from node_manager.exc.exceptions import AlreadyExistException, NoSuchEnvironment
from node_manager.models import models_environments
from node_manager.schemas import schemas_environments
from node_manager.crud.crud_platforms import get_platform_by_name


async def get_environment(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    if is_uuid(environment):
        environment = await get_environment_by_id(
            platform_name=platform_name,
            environment_id=environment,
            session=session
        )
        return environment

    environment = await get_environment_by_name(
        platform_name=platform_name,
        environment_name=environment,
        session=session
    )

    return environment


async def get_platform_environments(
    platform_name: str,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(
        platform_name=platform_name,
        session=session
    )

    query_environments = select(
        models_environments.Environment
    ).where(
        models_environments.Environment.platform_id == platform.id
    )

    result_query_environments = await session.execute(query_environments)
    environments = result_query_environments.scalars().all()

    return environments


async def add_new_environment(
        new_environment: schemas_environments.EnvironmentCreate,
        platform_name: str,
        session: AsyncSession
) -> bool | None:

    platform = await get_platform_by_name(platform_name=platform_name, session=session)
    new_environment.name = title_to_lowercase(title=new_environment.name)
    query = insert(models_environments.Environment).values(**new_environment.dict(), platform_id=platform.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Environment with such name in {platform_name} platform already exist')

    await session.commit()
    return True


async def get_environment_by_id(
        platform_name: str,
        environment_id: UUID,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    query_environments = select(
        models_environments.Environment
    ).where(
        models_environments.Environment.id == environment_id and
        models_environments.Environment.platform_id == platform.id,
    )

    result_query_environments = await session.execute(query_environments)
    environment = result_query_environments.scalars().first()

    if not environment:
        raise NoSuchEnvironment(f'Environment with id {environment_id} does not '
                                f'exist in platform with name {platform_name}')

    return environment


async def delete_environment_by_id(
        environment_id: UUID,
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


async def get_environment_by_name(
        platform_name: str,
        environment_name: str,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    query_environments = select(
        models_environments.Environment
    ).where(
        models_environments.Environment.name == environment_name and
        models_environments.Environment.platform_id == platform.id,
    )

    result_query_environments = await session.execute(query_environments)
    environment = result_query_environments.scalars().first()

    if not environment:
        raise NoSuchEnvironment(f'Environment with name "{environment_name}" does not '
                                f'exist in platform with name "{platform_name}"')

    return environment


async def delete_environment_by_name(
        environment_name: str,
        platform_name: str,
        session: AsyncSession
) -> bool:
    environment = await get_environment_by_name(
        environment_name=environment_name,
        platform_name=platform_name,
        session=session
    )

    if not environment:
        raise NoSuchEnvironment(f'Environment with name "{environment_name}" does not '
                                f'exist in platform with name "{platform_name}"')

    await session.delete(environment)
    await session.commit()
    return True
