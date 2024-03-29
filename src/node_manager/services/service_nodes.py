from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token
from modules.exc.exceptions.exceptions_nodes import NodeSnapshotError
from node_manager.crud import crud_nodes
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.crud.crud_nodes import (create_or_update_snapshot, delete_snapshot, get_snapshot,
                                          delete_node_snapshots, delete_all_snapshots, delete_all_node_platforms_links)
from node_manager.manager_config import SSH_PUBLIC_KEY
from node_manager.schemas import schemas_nodes
from node_manager.schemas.schemas_node_auth import TokenData
from node_manager.schemas.schemas_nodes import NodeRead, NodePlatformRead, NodeSnapshotRead
from node_manager.schemas.schemas_platforms import PlatformRead


async def get_all_nodes(
        **kwargs
) -> GenericResponseModel[List[NodeRead]]:
    data = await crud_nodes.get_nodes(
        **kwargs
    )

    return GenericResponseModel(data=data, total=len(data))


async def get_node(
        **kwargs
) -> GenericResponseModel[NodeRead]:
    data = await crud_nodes.get_node_by_id(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def create_node(
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession

) -> GenericResponseModel[NodeRead]:
    node = new_node.dict()
    token_expire = node.pop('token_expire')

    token_data = TokenData(
        node_name=new_node.name,
        server_ipv4=new_node.server_ipv4,
        server_pub_key=SSH_PUBLIC_KEY
    )
    token = create_access_token(
        data=token_data.dict(),
        expire=token_expire
    )

    node['token'] = token

    node = await crud_nodes.add_new_node(
        new_node=node,
        session=session
    )

    return GenericResponseModel(data=node)


async def delete_node(
        **kwargs
) -> GenericResponseModel[bool]:
    data = await crud_nodes.delete_node_by_id(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def change_node_status(
        **kwargs
) -> GenericResponseModel[bool]:
    data = await crud_nodes.change_status(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def get_node_status(
        **kwargs
) -> GenericResponseModel[bool]:
    data = await crud_nodes.get_status(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def get_node_platforms(
        **kwargs
) -> GenericResponseModel[List[PlatformRead]]:
    data = await crud_nodes.get_platforms(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def add_node_platform_link(
        **kwargs
) -> GenericResponseModel[NodePlatformRead]:
    data = await crud_nodes.create_node_platform(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def delete_node_platform_link(
        **kwargs
) -> GenericResponseModel[bool]:
    data = await crud_nodes.delete_node_platform(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def delete_node_platform_links(
        **kwargs
) -> GenericResponseModel[bool]:
    data = await crud_nodes.delete_all_node_platform_links(
        **kwargs
    )

    return GenericResponseModel(data=data)


async def get_node_platform_snapshot(
        **kwargs
) -> GenericResponseModel[NodeSnapshotRead]:
    snapshot = await get_snapshot(
        **kwargs
    )

    if snapshot is None:
        raise NodeSnapshotError('No such snapshot')

    return GenericResponseModel(data=snapshot)


async def create_or_update_platform_snapshot(
        **kwargs
) -> GenericResponseModel[NodeSnapshotRead]:
    created_snapshot = await create_or_update_snapshot(
        **kwargs
    )

    return GenericResponseModel(data=created_snapshot)


async def delete_platform_snapshot(
        **kwargs
) -> GenericResponseModel[bool]:
    snapshot = await delete_snapshot(
        **kwargs
    )

    return GenericResponseModel(data=snapshot)


async def delete_all_node_snapshots(
        **kwargs
) -> GenericResponseModel[bool]:
    snapshot = await delete_node_snapshots(
        **kwargs
    )

    return GenericResponseModel(data=snapshot)


async def delete_node_platforms_links(
        **kwargs
) -> GenericResponseModel[bool]:
    snapshot = await delete_all_node_platforms_links(
        **kwargs
    )

    return GenericResponseModel(data=snapshot)


async def delete_all_nodes_snapshots(
        **kwargs
) -> GenericResponseModel[bool]:
    snapshot = await delete_all_snapshots(
        **kwargs
    )

    return GenericResponseModel(data=snapshot)
