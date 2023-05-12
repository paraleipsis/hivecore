from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database.session import get_async_session
from modules.schemas.schemas_docker_snapshot import DockerSnapshot, SwarmSnapshot
from node_manager.schemas import schemas_nodes
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.schemas.schemas_nodes import NodePlatformRead
from node_manager.schemas.schemas_platforms import PlatformRead
from node_manager.services import service_nodes


router = APIRouter(
    prefix='/nodes',
    tags=['Nodes']
)


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_nodes.NodeRead]]
)
async def get_all_nodes_request(
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_all_nodes(
        session=session,
    )


@router.get(
    '/{node_id}',
    response_model=GenericResponseModel[schemas_nodes.NodeRead]
)
async def get_node_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node(
        session=session,
        node_id=node_id,
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_nodes.NodeRead]
)
async def create_node_request(
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.create_node(
        session=session,
        new_node=new_node
    )


@router.delete(
    '/{node_id}',
    response_model=GenericResponseModel[bool],
)
async def delete_node_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node(
        session=session,
        node_id=node_id
    )


@router.get(
    '/{node_id}/status',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def get_node_status_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node_status(
        session=session,
        node_id=node_id,
    )


@router.patch(
    '/{node_id}/status',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def change_node_status_request(
        node_id: UUID,
        new_status: bool,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.change_node_status(
        session=session,
        node_id=node_id,
        new_status=new_status
    )


@router.get(
    '/{node_id}/platforms',
    response_model=GenericResponseModel[List[PlatformRead]]
)
async def get_node_platforms_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node_platforms(
        session=session,
        node_id=node_id,
    )


@router.post(
    '/{node_id}/platforms',
    response_model=GenericResponseModel[NodePlatformRead],
    # include_in_schema=False
)
async def add_node_platform_link_request(
        node_id: UUID,
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.add_node_platform_link(
        session=session,
        platform_name=platform_name,
        node_id=node_id
    )


@router.delete(
    '/{node_id}/platforms/{platform_name}',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_node_platform_link_request(
        platform_name: str,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node_platform_link(
        session=session,
        platform_name=platform_name,
        node_id=node_id
    )


@router.delete(
    '/{node_id}/platforms',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_node_platforms_links_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node_platforms_links(
        session=session,
        node_id=node_id
    )


@router.delete(
    '/platforms',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_all_node_platform_links_request(
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node_platform_links(
        session=session,
    )


@router.get(
    '/{node_id}/snapshots/{platform_name}',
    response_model=GenericResponseModel[schemas_nodes.NodeSnapshotRead]
)
async def get_node_platform_snapshot_request(
        node_id: UUID,
        platform_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node_platform_snapshot(
        session=session,
        node_id=node_id,
        platform_name=platform_name
    )


@router.put(
    '/{node_id}/snapshots/{platform_name}',
    response_model=GenericResponseModel[schemas_nodes.NodeSnapshotRead],
    # include_in_schema=False
)
async def create_or_update_snapshot_request(
        platform_name: str,
        node_id: UUID,
        snapshot: DockerSnapshot | SwarmSnapshot,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.create_or_update_platform_snapshot(
        session=session,
        platform_name=platform_name,
        node_id=node_id,
        snapshot=snapshot
    )


@router.delete(
    '/{node_id}/snapshots/{platform_name}',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_snapshot_node_request(
        platform_name: str,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_platform_snapshot(
        session=session,
        platform_name=platform_name,
        node_id=node_id
    )


@router.delete(
    '/{node_id}/snapshots',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_snapshots_node_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_all_node_snapshots(
        session=session,
        node_id=node_id
    )


@router.delete(
    '/snapshots',
    response_model=GenericResponseModel[bool],
    # include_in_schema=False
)
async def delete_all_snapshots_request(
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_all_nodes_snapshots(
        session=session,
    )
