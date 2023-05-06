from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from docker.schemas.schemas_system import (AuthCredentials, SystemVersion, SystemDF, SystemInfo,
                                           AuthToken, AuthError)
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_system import (get_system_df_from_db, get_system_df_from_broker,
                                            get_docker_version_from_db, get_system_info_from_db,
                                            get_system_info_from_broker, prune_docker_system,
                                            check_auth_conf, get_docker_events)


router = APIRouter(
    prefix='/docker/{node_id}/system',
    tags=['Docker System']
)

websocket_manager = ConnectionManager()


@router.get(
    '/info/json',
    response_model=GenericResponseModel[SystemInfo]
)
async def get_system_info_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_system_info_from_db(
        node_id=node_id,
        session=session
    )


@router.get(
    '/df/json',
    response_model=GenericResponseModel[SystemDF]
)
async def get_system_df_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_system_df_from_db(
        node_id=node_id,
        session=session,
    )


@router.websocket(
    '/info/ws',
)
async def get_system_info_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_system_info_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for info in get_system_info_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=info.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/df/ws',
)
async def get_system_df_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_system_df_from_db(
            node_id=node_id,
            session=session,
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for df in get_system_df_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=df.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.get(
    '/version/json',
    response_model=GenericResponseModel[SystemVersion]
)
async def get_system_version_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_docker_version_from_db(
        node_id=node_id,
        session=session,
    )


@router.post(
    '/auth',
    response_model=GenericResponseModel[Optional[Union[AuthToken, AuthError]]]
)
async def docker_login_request(
        node_id: UUID,
        config: AuthCredentials,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await check_auth_conf(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config
    )


@router.websocket(
    '/events',
)
async def system_events_request(
        websocket: WebSocket,
        node_id: UUID,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        async for message in get_docker_events(
                rssh_client=rssh_client,
                host_uuid=node_id
        ):
            await websocket_manager.send_json(
                message=message,
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.post(
    '/prune',
    response_model=GenericResponseModel
)
async def prune_system_request(
        node_id: UUID,
        volumes: bool = False,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await prune_docker_system(
        rssh_client=rssh_client,
        host_uuid=node_id,
        volumes=volumes
    )
