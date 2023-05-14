from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database.session import get_async_session
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.schemas.schemas_node_auth import NodeCredentials
from node_manager.services.service_node_auth import verify_node


router = APIRouter(
    prefix='/nodes/auth',
    tags=['Node Authentication']
)


@router.post(
    '',
    response_model=GenericResponseModel[bool]
)
async def login(
        node_credentials: NodeCredentials,
        session: AsyncSession = Depends(get_async_session)
):
    return await verify_node(
        session=session,
        node_credentials=node_credentials,
    )
