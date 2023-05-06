from typing import List, Optional, Union, MutableMapping
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from docker.schemas.schemas_containers import ContainerInspect, ContainerCreate
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_containers import (start_container_by_id, stop_container_by_id, restart_container_by_id,
                                                pause_container_by_id, unpause_container_by_id, kill_container_by_id,
                                                prune_stopped_containers, get_all_containers_from_db,
                                                get_all_containers_from_broker, get_container_from_db,
                                                get_container_from_broker, remove_container_by_id, logs_container_by_id,
                                                stats_container_by_id, run_new_container)

router = APIRouter(
    prefix='/docker/{node_id}/containers',
    tags=['Docker Containers']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[ContainerInspect]]
)
async def get_all_containers_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_all_containers_from_db(
        node_id=node_id,
        session=session
    )


@router.websocket(
    '/ws',
)
async def get_all_containers_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_all_containers_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for containers in get_all_containers_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=containers.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.get(
    '/{container_id}/json',
    response_model=GenericResponseModel[ContainerInspect]
)
async def get_container_request(
        node_id: UUID,
        container_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_container_from_db(
        node_id=node_id,
        session=session,
        container_id=container_id,
    )


@router.post(
    '/run',
    response_model=GenericResponseModel
)
async def run_container_request(
        node_id: UUID,
        config: ContainerCreate,
        name: Optional[str] = None,
        auth: Optional[Union[MutableMapping, str, bytes]] = None,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await run_new_container(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config,
        name=name,
        auth=auth
    )


@router.delete(
    '/{container_id}',
    response_model=GenericResponseModel
)
async def remove_container_request(
        node_id: UUID,
        container_id: str,
        volumes: bool = False,
        link: bool = False,
        force: bool = False,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await remove_container_by_id(
        host_uuid=node_id,
        container_id=container_id,
        rssh_client=rssh_client,
        v=volumes,
        link=link,
        force=force,
    )


@router.websocket(
    '/{container_id}/ws',
)
async def get_container_ws(
        websocket: WebSocket,
        node_id: UUID,
        container_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_container_from_db(
            node_id=node_id,
            session=session,
            container_id=container_id
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for container in get_container_from_broker(
                node_id=node_id,
                container_id=container_id
        ):
            await websocket_manager.send_json(
                message=container.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.post(
    '/{container_id}/start',
    response_model=GenericResponseModel
)
async def start_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await start_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{container_id}/stop',
    response_model=GenericResponseModel
)
async def stop_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await stop_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{container_id}/restart',
    response_model=GenericResponseModel
)
async def restart_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await restart_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{container_id}/pause',
    response_model=GenericResponseModel
)
async def pause_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await pause_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{container_id}/unpause',
    response_model=GenericResponseModel
)
async def unpause_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await unpause_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/{container_id}/kill',
    response_model=GenericResponseModel
)
async def kill_container_request(
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await kill_container_by_id(
        container_id=container_id,
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/prune',
    response_model=GenericResponseModel
)
async def prune_containers_request(
        node_id: UUID,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await prune_stopped_containers(
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.websocket(
    '/{container_id}/logs',
)
async def logs_container_request(
        websocket: WebSocket,
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        async for message in logs_container_by_id(
                container_id=container_id,
                rssh_client=rssh_client,
                host_uuid=node_id
        ):
            await websocket_manager.send_str(
                message=message,
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/{container_id}/stats',
)
async def stats_container_request(
        websocket: WebSocket,
        node_id: UUID,
        container_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        async for message in stats_container_by_id(
                container_id=container_id,
                rssh_client=rssh_client,
                host_uuid=node_id
        ):
            await websocket_manager.send_json(
                message=message.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()
