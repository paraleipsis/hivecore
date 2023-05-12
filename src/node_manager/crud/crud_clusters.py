from typing import Any, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Row, RowMapping
from sqlalchemy.exc import IntegrityError

from modules.exc.exceptions.exceptions import AlreadyExistException
from modules.exc.exceptions.exceptions_clusters import NoSuchCluster
from node_manager.models import models_clusters
from node_manager.schemas import schemas_clusters
from node_manager.crud.crud_platforms import get_platform_by_name


async def get_platform_clusters(
    platform_name: str,
    session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(
        platform_name=platform_name,
        session=session
    )

    query_cluster = select(
        models_clusters.Cluster
    ).where(
        models_clusters.Cluster.platform_id == platform.id
    )

    result_query_clusters = await session.execute(query_cluster)
    clusters = result_query_clusters.scalars().all()

    return clusters


async def add_new_cluster(
        new_cluster: schemas_clusters.ClusterCreate,
        platform_name: str,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:

    platform = await get_platform_by_name(
        platform_name=platform_name,
        session=session
    )
    query = insert(
        models_clusters.Cluster
    ).values(
        **new_cluster.dict(), platform_id=platform.id
    ).returning(
        models_clusters.Cluster.id
    )

    try:
        result = await session.execute(query)
    except IntegrityError:
        raise AlreadyExistException(f'Cluster with such id in {platform_name} platform already exist')

    await session.commit()

    cluster_id = result.scalar()
    cluster = await get_cluster_by_id(
        platform_name=platform_name,
        cluster_id=cluster_id,
        session=session
    )

    return cluster


async def get_cluster_by_id(
        platform_name: str,
        cluster_id: UUID,
        session: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    platform = await get_platform_by_name(platform_name=platform_name, session=session)

    query_clusters = select(
        models_clusters.Cluster
    ).where(
        models_clusters.Cluster.id == cluster_id and
        models_clusters.Cluster.platform_id == platform.id,
    )

    result_query_cluster = await session.execute(query_clusters)
    cluster = result_query_cluster.scalars().first()

    if not cluster:
        raise NoSuchCluster(f'Cluster with id {cluster_id} does not '
                            f'exist in platform with name {platform_name}')

    return cluster


async def delete_cluster_by_id(
        cluster_id: UUID,
        platform_name: str,
        session: AsyncSession
) -> bool:
    cluster = await get_cluster_by_id(
        cluster_id=cluster_id,
        platform_name=platform_name,
        session=session
    )

    if not cluster:
        raise NoSuchCluster(f'Cluster with id {cluster_id} does not '
                            f'exist in platform with name {platform_name}')

    await session.delete(cluster)
    await session.commit()

    return True
