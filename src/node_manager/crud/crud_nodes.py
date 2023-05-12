from typing import Any, Sequence, Union
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, Row, RowMapping, delete
from sqlalchemy.orm import selectinload

from modules.exc.exceptions.exceptions_nodes import NoSuchNode, PlatformNodeLinkError
from modules.schemas.schemas_docker_snapshot import DockerSnapshot, SwarmSnapshot
from node_manager.models import models_nodes, Node, platform_nodes, Snapshot
from node_manager.schemas import schemas_nodes


async def get_nodes(
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(models_nodes.Node)
    result = await session.execute(query)
    nodes = result.scalars().all()

    return nodes


async def get_node_by_id(
    node_id: UUID,
    session: AsyncSession
) -> Node:
    query = select(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id
    ).options(selectinload(Node.platforms))

    result = await session.execute(query)
    node = result.scalars().first()

    return node


async def add_new_node(
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession
) -> Node:
    query = insert(
        models_nodes.Node
    ).values(
        **new_node.dict()
    ).returning(
        models_nodes.Node.id
    )

    result = await session.execute(query)
    await session.commit()

    node_id = result.scalar()
    node = await get_node_by_id(node_id=node_id, session=session)

    return node


async def delete_node_by_id(
        node_id: UUID,
        session: AsyncSession
) -> bool:
    node = await get_node_by_id(
        node_id=node_id,
        session=session
    )

    if not node:
        raise NoSuchNode(f'Node with id {node_id} does not exist')

    await session.delete(node)
    await session.commit()

    return True


async def change_status(
        node_id: UUID,
        new_status: bool,
        session: AsyncSession
):
    query_nodes = update(
        models_nodes.Node
    ).where(
        models_nodes.Node.id == node_id
    ).values(
        active=new_status
    )

    await session.execute(query_nodes)
    await session.commit()

    return True


async def get_status(
        node_id: UUID,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    node = await get_node_by_id(
        node_id=node_id,
        session=session
    )

    return node.active


async def get_platforms(
    node_id: UUID,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    node = await get_node_by_id(
        node_id=node_id,
        session=session
    )

    return node.platforms


async def get_node_platform_by_id(
    node_platform_id: UUID,
    session: AsyncSession,
) -> platform_nodes:
    query = select(
        platform_nodes
    ).where(
        platform_nodes.c.id == node_platform_id
    )

    result = await session.execute(query)
    node_platform_link = result.first()

    return node_platform_link


async def create_node_platform(
    node_id: UUID,
    platform_name: str,
    session: AsyncSession,
) -> platform_nodes:
    query = insert(
        platform_nodes
    ).values(
        node_id=node_id,
        platform_name=platform_name
    ).returning(
        platform_nodes.c.id
    )

    try:
        result = await session.execute(query)
        await session.commit()
        node_platform_link = await get_node_platform_by_id(
            node_platform_id=result.scalar(),
            session=session
        )

        return node_platform_link
    except IntegrityError:
        raise PlatformNodeLinkError('Node with such ID or Platform with such name does not exist')


async def delete_node_platform(
        node_id: UUID,
        platform_name: str,
        session: AsyncSession
) -> bool:
    query = delete(
        platform_nodes
    ).where(
        platform_nodes.c.node_id == node_id,
        platform_nodes.c.platform_name == platform_name
    ).returning(
        platform_nodes.c.id
    )

    result = await session.execute(query)
    await session.commit()

    if result.scalar() is None:
        raise PlatformNodeLinkError('Node with such ID or Platform with such name does not exist')

    return True


async def delete_all_node_platforms_links(
        node_id: UUID,
        session: AsyncSession
) -> bool:
    query = delete(
        platform_nodes
    ).where(
        platform_nodes.c.node_id == node_id
    ).returning(
        platform_nodes.c.id
    )

    result = await session.execute(query)
    await session.commit()

    if result.scalar() is None:
        raise PlatformNodeLinkError('Node with such ID does not exist')

    return True


async def get_snapshot_by_id(
        snapshot_id: UUID,
        session: AsyncSession
) -> Snapshot:
    query = select(
        Snapshot
    ).where(
        Snapshot.id == snapshot_id
    )

    result = await session.execute(query)
    snapshot = result.scalars().first()

    return snapshot


async def get_snapshot(
        node_id: UUID,
        platform_name: str,
        session: AsyncSession
) -> Snapshot:
    query = select(
        Snapshot
    ).where(
        Snapshot.platform_name == platform_name and
        Snapshot.node_id == node_id
    )

    result = await session.execute(query)
    snapshot = result.scalars().first()

    return snapshot


async def create_snapshot(
        node_id: UUID,
        platform_name: str,
        new_snapshot: Union[SwarmSnapshot, DockerSnapshot],
        session: AsyncSession
) -> Snapshot:
    query = insert(
        Snapshot
    ).values(
        node_id=node_id,
        platform_name=platform_name,
        snapshot=new_snapshot.dict()
    ).returning(
        Snapshot.id
    )

    result = await session.execute(query)
    await session.commit()

    snapshot_id = result.scalar()
    snapshot = await get_snapshot_by_id(
        snapshot_id=snapshot_id,
        session=session
    )

    return snapshot


async def update_snapshot(
        node_id: UUID,
        platform_name: str,
        new_snapshot: Union[SwarmSnapshot, DockerSnapshot],
        session: AsyncSession
) -> Snapshot:
    query = update(
        Snapshot
    ).where(
        Snapshot.node_id == node_id,
        Snapshot.platform_name == platform_name
    ).values(
        snapshot=new_snapshot.dict()
    ).returning(
        Snapshot.id
    )

    result = await session.execute(query)
    await session.commit()

    snapshot_id = result.scalar()
    snapshot = await get_snapshot_by_id(
        snapshot_id=snapshot_id,
        session=session
    )

    return snapshot


async def create_or_update_snapshot(
        platform_name: str,
        node_id: UUID,
        snapshot: Union[SwarmSnapshot, DockerSnapshot],
        session: AsyncSession
) -> Snapshot:
    try:
        existing_snapshot = await get_snapshot(
            node_id=node_id,
            platform_name=platform_name,
            session=session
        )

        if existing_snapshot:
            updated_snapshot = await update_snapshot(
                node_id=node_id,
                platform_name=platform_name,
                new_snapshot=snapshot,
                session=session
            )

            return updated_snapshot

        snapshot = await create_snapshot(
            node_id=node_id,
            platform_name=platform_name,
            new_snapshot=snapshot,
            session=session
        )
    except IntegrityError:
        raise PlatformNodeLinkError('Node with such ID or Platform with such name does not exist')

    return snapshot


async def delete_snapshot(
        node_id: UUID,
        platform_name: str,
        session: AsyncSession
) -> bool:
    query = delete(
        Snapshot
    ).where(
        Snapshot.platform_name == platform_name and
        Snapshot.node_id == node_id
    ).returning(
        Snapshot.id
    )

    result = await session.execute(query)
    await session.commit()

    if result.scalar() is None:
        raise PlatformNodeLinkError('Snapshot for this Node and Platform does not exist')

    return True


async def delete_node_snapshots(
        node_id: UUID,
        session: AsyncSession
) -> bool:
    query = delete(
        Snapshot
    ).where(
        Snapshot.node_id == node_id
    ).returning(
        Snapshot.id
    )

    result = await session.execute(query)
    await session.commit()

    if result.scalar() is None:
        raise PlatformNodeLinkError('Snapshots for this Node does not exist')

    return True


async def delete_all_snapshots(
        session: AsyncSession
) -> bool:
    query = delete(
        Snapshot
    )

    await session.execute(query)
    await session.commit()

    return True


async def delete_all_node_platform_links(
        session: AsyncSession
) -> bool:
    query = delete(
        platform_nodes
    )

    await session.execute(query)
    await session.commit()

    return True
