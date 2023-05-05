from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from docker.schemas.schemas_networks import (NetworkInspect, NetworkCreate, NetworkConnectContainer,
                                             NetworkDisconnectContainer)
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_networks import (get_all_networks_from_db, get_network_from_db,
                                              get_all_networks_from_broker, get_network_from_broker,
                                              remove_network_by_id, create_new_network, prune_unused_networks,
                                              connect_container_to_network, disconnect_container_from_network)


router = APIRouter(
    prefix='/docker/{node_id}/networks',
    tags=['Docker Networks']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[NetworkInspect]]
)
async def get_all_networks_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_all_networks_from_db(
        node_id=node_id,
        session=session
    )


@router.get(
    '/{network_id}/json',
    response_model=GenericResponseModel[NetworkInspect]
)
async def get_network_request(
        node_id: UUID,
        network_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_network_from_db(
        node_id=node_id,
        session=session,
        network_id=network_id
    )


@router.websocket(
    '/ws',
)
async def get_all_networks_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_all_networks_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for networks in get_all_networks_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=networks.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/{network_id}/ws',
)
async def get_network_ws(
        websocket: WebSocket,
        node_id: UUID,
        network_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_network_from_db(
            node_id=node_id,
            session=session,
            network_id=network_id
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for network in get_network_from_broker(
                node_id=node_id,
                network_id=network_id
        ):
            await websocket_manager.send_json(
                message=network.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.delete(
    '/{network_id}',
    response_model=GenericResponseModel
)
async def remove_network_request(
        node_id: UUID,
        network_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await remove_network_by_id(
        host_uuid=node_id,
        network_id=network_id,
        rssh_client=rssh_client,
    )


@router.post(
    '/create',
    response_model=GenericResponseModel
)
async def create_network_request(
        node_id: UUID,
        config: NetworkCreate,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await create_new_network(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config
    )


@router.post(
    '/prune',
    response_model=GenericResponseModel
)
async def prune_networks_request(
        node_id: UUID,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await prune_unused_networks(
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{network_id}/connect',
    response_model=GenericResponseModel
)
async def connect_network_request(
        node_id: UUID,
        network_id: str,
        config: NetworkConnectContainer,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await connect_container_to_network(
        rssh_client=rssh_client,
        host_uuid=node_id,
        network_id=network_id,
        config=config
    )


@router.post(
    '/{network_id}/disconnect',
    response_model=GenericResponseModel
)
async def disconnect_network_request(
        node_id: UUID,
        network_id: str,
        config: NetworkDisconnectContainer,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await disconnect_container_from_network(
        rssh_client=rssh_client,
        host_uuid=node_id,
        network_id=network_id,
        config=config
    )
