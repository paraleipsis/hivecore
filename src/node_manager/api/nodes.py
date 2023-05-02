from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database.session import get_async_session
from node_manager.schemas import schemas_nodes
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.services import service_nodes


router = APIRouter(
    prefix='/platforms/{platform_name}/environments/{environment}/nodes',
    tags=['Nodes']
)


@router.get(
    '/',
    response_model=GenericResponseModel[List[schemas_nodes.NodeRead]]
)
async def get_all_nodes_request(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_all_nodes(
        session=session,
        platform_name=platform_name,
        environment=environment
    )


@router.get(
    '/{node_id}',
    response_model=GenericResponseModel[schemas_nodes.NodeRead]
)
async def get_node_request(
        node_id: UUID,
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node(
        session=session,
        node_id=node_id,
        platform_name=platform_name,
        environment=environment
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_nodes.NodeCreate]
)
async def create_node_request(
        platform_name: str,
        environment: str | UUID,
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.create_node(
        session=session,
        platform_name=platform_name,
        environment=environment,
        new_node=new_node
    )


@router.delete(
    '/{node_id}',
    response_model=GenericResponseModel[bool]
)
async def delete_node_request(
        platform_name: str,
        environment: str | UUID,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node(
        session=session,
        platform_name=platform_name,
        environment=environment,
        node_id=node_id
    )
