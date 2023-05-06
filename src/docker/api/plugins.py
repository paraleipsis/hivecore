from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from docker.schemas.schemas_plugins import (PluginInspect, PluginInstall)
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_plugins import (get_all_plugins_from_db, get_plugin_from_db,
                                             get_all_plugins_from_broker, get_plugin_from_broker,
                                             remove_plugin_by_id, install_new_plugin, enable_plugin_by_id,
                                             disable_plugin_by_id)


router = APIRouter(
    prefix='/docker/{node_id}/plugins',
    tags=['Docker Plugins']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[PluginInspect]]
)
async def get_all_plugins_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_all_plugins_from_db(
        node_id=node_id,
        session=session
    )


@router.get(
    '/{plugin_id}/json',
    response_model=GenericResponseModel[PluginInspect]
)
async def get_plugin_request(
        node_id: UUID,
        plugin_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_plugin_from_db(
        node_id=node_id,
        session=session,
        plugin_id=plugin_id
    )


@router.websocket(
    '/ws',
)
async def get_all_plugins_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_all_plugins_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for plugins in get_all_plugins_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=plugins.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/{plugin_id}/ws',
)
async def get_plugin_ws(
        websocket: WebSocket,
        node_id: UUID,
        plugin_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_plugin_from_db(
            node_id=node_id,
            session=session,
            plugin_id=plugin_id
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for plugin in get_plugin_from_broker(
                node_id=node_id,
                plugin_id=plugin_id
        ):
            await websocket_manager.send_json(
                message=plugin.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.delete(
    '/{plugin_id}',
    response_model=GenericResponseModel
)
async def remove_plugin_request(
        node_id: UUID,
        plugin_id: str,
        force: bool = False,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await remove_plugin_by_id(
        host_uuid=node_id,
        plugin_id=plugin_id,
        rssh_client=rssh_client,
        force=force
    )


@router.post(
    '/install',
    response_model=GenericResponseModel
)
async def install_plugin_request(
        node_id: UUID,
        config: List[PluginInstall],
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await install_new_plugin(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config
    )


@router.post(
    '/{plugin_id}/enable',
    response_model=GenericResponseModel
)
async def enable_plugin_request(
        node_id: UUID,
        plugin_id: str,
        timeout: int = 0,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await enable_plugin_by_id(
        rssh_client=rssh_client,
        host_uuid=node_id,
        plugin_id=plugin_id,
        timeout=timeout
    )


@router.post(
    '/{plugin_id}/disable',
    response_model=GenericResponseModel
)
async def disable_plugin_request(
        node_id: UUID,
        plugin_id: str,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await disable_plugin_by_id(
        rssh_client=rssh_client,
        host_uuid=node_id,
        plugin_id=plugin_id,
    )
