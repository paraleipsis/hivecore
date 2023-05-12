from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_clusters
from node_manager.crud import crud_clusters
from modules.schemas.schemas_response import GenericResponseModel


async def get_all_clusters(
        platform_name: str,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_clusters.get_platform_clusters(
        platform_name=platform_name,
        session=session
    )

    return GenericResponseModel(data=data, total=len(data))


async def get_cluster(
        platform_name: str,
        cluster_id: UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_clusters.get_cluster_by_id(
        cluster_id=cluster_id,
        platform_name=platform_name,
        session=session
    )

    return GenericResponseModel(data=data, total=1)


async def create_cluster(
        platform_name: str,
        new_cluster: schemas_clusters.ClusterCreate,
        session: AsyncSession
) -> GenericResponseModel:
    cluster = await crud_clusters.add_new_cluster(
        new_cluster=new_cluster,
        session=session,
        platform_name=platform_name
    )

    return GenericResponseModel(data=cluster)


async def delete_cluster(
        platform_name: str,
        cluster_id: UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_clusters.delete_cluster_by_id(
        platform_name=platform_name,
        cluster_id=cluster_id,
        session=session
    )

    return GenericResponseModel(data=data)

