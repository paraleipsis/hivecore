from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database.session import get_async_session
from node_manager.schemas import schemas_clusters
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.services import service_clusters


router = APIRouter(
    prefix='/platforms/{platform_name}/clusters',
    tags=['Clusters']
)


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_clusters.ClusterRead]]
)
async def get_all_clusters_request(
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_clusters.get_all_clusters(
        session=session,
        platform_name=platform_name
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_clusters.ClusterRead]
)
async def create_cluster_request(
        platform_name: str,
        new_cluster: schemas_clusters.ClusterCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_clusters.create_cluster(
        session=session,
        platform_name=platform_name,
        new_cluster=new_cluster
    )


@router.get(
    '/{cluster_id}',
    response_model=GenericResponseModel[schemas_clusters.ClusterRead]
)
async def get_cluster_request(
        platform_name: str,
        cluster_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_clusters.get_cluster(
        session=session,
        platform_name=platform_name,
        cluster_id=cluster_id
    )


@router.delete(
    '/{cluster_id}',
    response_model=GenericResponseModel[bool]
)
async def delete_cluster_request(
        platform_name: str,
        cluster_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_clusters.delete_cluster(
        session=session,
        platform_name=platform_name,
        cluster_id=cluster_id
    )
