from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_nodes
from node_manager.crud import crud_environments, crud_nodes
from schemas.response_schemas import GenericResponseModel


async def get_all_nodes(
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_environments.get_environment_by_id(
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data, total=len(data.nodes))


async def get_node(
        node_id: int,
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_nodes.get_node_by_id(
        node_id=node_id,
        environment_id=environment_id,
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data)


async def create_node(
        platform_name: str,
        environment_id: int,
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession
) -> GenericResponseModel:
    await crud_nodes.add_new_node(
        new_node=new_node,
        environment_id=environment_id,
        session=session,
        platform_name=platform_name
    )
    return GenericResponseModel(data=new_node)


async def delete_node(
        platform_name: str,
        environment_id: int,
        node_id: int,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_nodes.delete_node_by_id(
        node_id=node_id,
        platform_name=platform_name,
        environment_id=environment_id,
        session=session
    )
    return GenericResponseModel(data=data)
