from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from docker.schemas.schemas_containers import ContainerInspect
from docker.services.service_containers import get_containers_from_db, get_containers_from_broker
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_containers import start_container_by_id

router = APIRouter(
    prefix='/docker/{node_id}/containers',
    tags=['Docker']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[ContainerInspect]]
)
async def get_containers_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_containers_from_db(
        node_id=node_id,
        session=session
    )


@router.websocket(
    '/ws',
)
async def get_containers_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_containers_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_message(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for containers in get_containers_from_broker(node_id=node_id):
            await websocket_manager.send_message(
                message=containers.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)


@router.get(
    '/{container_id}/start',
    response_model=GenericResponseModel
)
async def start_container(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await start_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )
