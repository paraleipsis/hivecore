from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from docker.schemas.schemas_volumes import (VolumeInspect, VolumeCreate)
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_volumes import (get_all_volumes_from_db, get_volume_from_db, get_all_volumes_from_broker,
                                             get_volume_from_broker, remove_volume_by_id, create_new_volume,
                                             prune_unused_volumes)


router = APIRouter(
    prefix='/docker/{node_id}/volumes',
    tags=['Docker Volumes']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[VolumeInspect]]
)
async def get_all_volumes_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_all_volumes_from_db(
        node_id=node_id,
        session=session
    )


@router.get(
    '/{volume_id}/json',
    response_model=GenericResponseModel[VolumeInspect]
)
async def get_volume_request(
        node_id: UUID,
        volume_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_volume_from_db(
        node_id=node_id,
        session=session,
        volume_id=volume_id
    )


@router.websocket(
    '/ws',
)
async def get_all_volumes_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_all_volumes_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for volumes in get_all_volumes_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=volumes.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/{volume_id}/ws',
)
async def get_volume_ws(
        websocket: WebSocket,
        node_id: UUID,
        volume_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_volume_from_db(
            node_id=node_id,
            session=session,
            volume_id=volume_id
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for volume in get_volume_from_broker(
                node_id=node_id,
                volume_id=volume_id
        ):
            await websocket_manager.send_json(
                message=volume.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.delete(
    '/{volume_id}',
    response_model=GenericResponseModel
)
async def remove_volume_request(
        node_id: UUID,
        volume_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await remove_volume_by_id(
        host_uuid=node_id,
        volume_id=volume_id,
        rssh_client=rssh_client,
    )


@router.post(
    '/create',
    response_model=GenericResponseModel
)
async def create_volume_request(
        node_id: UUID,
        config: VolumeCreate,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await create_new_volume(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config
    )


@router.post(
    '/prune',
    response_model=GenericResponseModel
)
async def prune_volumes_request(
        node_id: UUID,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await prune_unused_volumes(
        rssh_client=rssh_client,
        host_uuid=node_id
    )
