from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from node_manager.schemas import schemas_environments, schemas_nodes
from schemas.response_schemas import GenericResponseModel
from node_manager.services import service_nodes


router = APIRouter(
    prefix='/platforms/{platform_name}/environments/{environment_id}/nodes',
    tags=['Nodes']
)


@router.get(
    '/',
    response_model=GenericResponseModel[schemas_environments.EnvironmentDetailsRead]
)
async def get_all_nodes_request(
        platform_name: str,
        environment_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_all_nodes(
        session=session,
        platform_name=platform_name,
        environment_id=environment_id
    )


@router.get(
    '/{node_id}',
    response_model=GenericResponseModel[schemas_nodes.NodeRead]
)
async def get_node_request(
        node_id: int,
        platform_name: str,
        environment_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.get_node(
        session=session,
        node_id=node_id,
        platform_name=platform_name,
        environment_id=environment_id
    )


@router.post(
    '/',
    response_model=GenericResponseModel[schemas_nodes.NodeCreate]
)
async def create_node_request(
        platform_name: str,
        environment_id: int,
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.create_node(
        session=session,
        platform_name=platform_name,
        environment_id=environment_id,
        new_node=new_node
    )


@router.delete(
    '/{node_id}',
    response_model=GenericResponseModel[bool]
)
async def delete_node_request(
        platform_name: str,
        environment_id: int,
        node_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await service_nodes.delete_node(
        session=session,
        platform_name=platform_name,
        environment_id=environment_id,
        node_id=node_id
    )
