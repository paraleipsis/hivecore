from typing import Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.exc import IntegrityError

from node_manager.exc_handlers.exceptions import AlreadyExistException, NoSuchNode
from node_manager.models import models_nodes
from node_manager.schemas import schemas_nodes
from node_manager.crud.crud_environments import get_environment_by_id


async def get_node_by_id(
        node_id: int,
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    environment = await get_environment_by_id(
        platform_name=platform_name,
        environment_id=environment_id,
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
                         f'{environment_id} and platform with name {platform_name}')

    return node


async def add_new_node(
        new_node: schemas_nodes.NodeCreate,
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> bool | None:

    environment = await get_environment_by_id(
        platform_name=platform_name,
        environment_id=environment_id,
        session=session
    )
    query = insert(models_nodes.Node).values(**new_node.dict(), environment_id=environment.id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Node with such name in {platform_name} platform and '
                                    f'{environment_id} environment already exist')

    await session.commit()
    return True


async def delete_node_by_id(
        node_id: int,
        environment_id: int,
        platform_name: str,
        session: AsyncSession
) -> bool:
    node = await get_node_by_id(
        node_id=node_id,
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist in environment with id '
                         f'{environment_id} and platform with name {platform_name}')

    await session.delete(node)
    await session.commit()
    return True
