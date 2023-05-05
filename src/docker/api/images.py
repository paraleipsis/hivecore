from typing import List, Optional, Union, MutableMapping
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from db.database.session import get_async_session
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_response import GenericResponseModel
from docker.schemas.schemas_images import ImageInspect, ImageCreate
from modules.websocket.manager import ConnectionManager
from rssh_client.rssh import get_rssh_client
from docker.services.service_images import (build_new_image, get_all_images_from_db, get_all_images_from_broker,
                                            prune_unused_images, pull_new_image, tag_image_repo, remove_image_by_id,
                                            get_image_from_db, get_image_from_broker)


router = APIRouter(
    prefix='/docker/{node_id}/images',
    tags=['Docker Images']
)

websocket_manager = ConnectionManager()


@router.get(
    '/json',
    response_model=GenericResponseModel[List[ImageInspect]]
)
async def get_all_images_request(
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_all_images_from_db(
        node_id=node_id,
        session=session
    )


@router.get(
    '/{image_id}/json',
    response_model=GenericResponseModel[ImageInspect]
)
async def get_image_request(
        node_id: UUID,
        image_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_image_from_db(
        node_id=node_id,
        session=session,
        images_id=image_id
    )


@router.websocket(
    '/ws',
)
async def get_all_images_ws(
        websocket: WebSocket,
        node_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_all_images_from_db(
            node_id=node_id,
            session=session
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for images in get_all_images_from_broker(node_id=node_id):
            await websocket_manager.send_json(
                message=images.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.websocket(
    '/{image_id}/ws',
)
async def get_image_ws(
        websocket: WebSocket,
        node_id: UUID,
        image_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    await websocket_manager.connect(websocket=websocket)
    try:
        initial_snapshot = await get_image_from_db(
            node_id=node_id,
            session=session,
            images_id=image_id
        )
        await websocket_manager.send_json(
            message=initial_snapshot.dict(),
            websocket=websocket
        )
        async for images in get_image_from_broker(
                node_id=node_id,
                image_id=image_id
        ):
            await websocket_manager.send_json(
                message=images.dict(),
                websocket=websocket
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket=websocket)
    finally:
        await websocket.close()


@router.delete(
    '/{image_id}',
    response_model=GenericResponseModel
)
async def remove_image_request(
        node_id: UUID,
        image_id: str,
        force: bool = False,
        noprune: bool = False,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await remove_image_by_id(
        host_uuid=node_id,
        image_id=image_id,
        rssh_client=rssh_client,
        noprune=noprune,
        force=force,
    )


@router.post(
    '/build',
    response_model=GenericResponseModel
)
async def build_image_request(
        node_id: UUID,
        config: ImageCreate,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await build_new_image(
        host_uuid=node_id,
        rssh_client=rssh_client,
        config=config
    )


@router.post(
    '/prune',
    response_model=GenericResponseModel
)
async def prune_images_request(
        node_id: UUID,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await prune_unused_images(
        rssh_client=rssh_client,
        host_uuid=node_id
    )


@router.post(
    '/pull',
    response_model=GenericResponseModel
)
async def pull_image_request(
        node_id: UUID,
        from_image: str,
        auth: Optional[Union[MutableMapping, str, bytes]] = None,
        tag: str = None,
        repo: str = None,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await pull_new_image(
        rssh_client=rssh_client,
        host_uuid=node_id,
        from_image=from_image,
        tag=tag,
        repo=repo,
        auth=auth
    )


@router.post(
    '/{image_id}/tag',
    response_model=GenericResponseModel
)
async def tag_image_request(
        node_id: UUID,
        image_id: str,
        repo: str,
        tag: str = None,
        rssh_client: ReverseSSHClient = Depends(get_rssh_client)
):
    return await tag_image_repo(
        rssh_client=rssh_client,
        host_uuid=node_id,
        image_id=image_id,
        repo=repo,
        tag=tag
    )
