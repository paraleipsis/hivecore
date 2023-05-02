from typing import Any, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.exc import IntegrityError

from node_manager.utils import title_to_lowercase
from node_manager.exc.exceptions import AlreadyExistException
from modules.exc.exceptions.exceptions_nodes import NoSuchNode
from modules.models import models_nodes
from node_manager.schemas import schemas_nodes
from node_manager.crud.crud_environments import get_environment


async def get_environment_nodes(
    platform_name: str,
    environment: str | UUID,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    environment = await get_environment(
        platform_name=platform_name,
        environment=environment,
        session=session
    )

    query_nodes = select(
        models_nodes.Node
    ).where(
        models_nodes.Node.environment_id == environment.id
    )

    result_query_nodes = await session.execute(query_nodes)
    nodes = result_query_nodes.scalars().all()

    return nodes


async def get_node_by_id(
    node_id: UUID,
    platform_name: str,
    environment: str | UUID,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    environment = await get_environment(
        platform_name=platform_name,
        environment=environment,
        session=session
    )

    query_nodes = select(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id and
        models_nodes.Node.environment_id == environment.id,
    )

    result_query_nodes = await session.execute(query_nodes)
    node = result_query_nodes.scalars().first()

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist in environment with id '
                         f'{environment.id} and platform with name {platform_name}')

    return node


async def add_new_node(
        new_node: schemas_nodes.NodeCreate,
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> bool | None:
    environment = await get_environment(
        platform_name=platform_name,
        environment=environment,
        session=session
    )

    new_node.name = title_to_lowercase(title=new_node.name)
    query = insert(models_nodes.Node).values(**new_node.dict(), environment_id=environment.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Node with such name in {platform_name} platform and '
                                    f'{environment.id} environment already exist')

    await session.commit()
    return True


async def delete_node_by_id(
        node_id: UUID,
        environment: str | UUID,
        platform_name: str,
        session: AsyncSession
) -> bool:
    node = await get_node_by_id(
        node_id=node_id,
        environment=environment,
        platform_name=platform_name,
        session=session
    )

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist in environment with id '
                         f'{environment.id} and platform with name {platform_name}')

    await session.delete(node)
    await session.commit()
    return True
