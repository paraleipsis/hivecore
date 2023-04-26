from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_nodes
from node_manager.crud import crud_nodes
from modules.schemas.response_schemas import GenericResponseModel


async def get_all_nodes(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_nodes.get_environment_nodes(
        platform_name=platform_name,
        environment=environment,
        session=session
    )

    return GenericResponseModel(data=data, total=len(data))


async def get_node(
        node_id: UUID,
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_nodes.get_node_by_id(
        node_id=node_id,
        environment=environment,
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data, total=1)


async def create_node(
        platform_name: str,
        environment: int | UUID,
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession
) -> GenericResponseModel:
    await crud_nodes.add_new_node(
        new_node=new_node,
        environment=environment,
        session=session,
        platform_name=platform_name
    )
    return GenericResponseModel(data=new_node)


async def delete_node(
        platform_name: str,
        environment: str | UUID,
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_nodes.delete_node_by_id(
        node_id=node_id,
        platform_name=platform_name,
        environment=environment,
        session=session
    )
    return GenericResponseModel(data=data)
