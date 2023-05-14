from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import verify_node_access_token
from modules.exc.exceptions.exceptions_node_auth import NodeAuthError
from modules.schemas.schemas_response import GenericResponseModel
from node_manager.crud import crud_nodes
from node_manager.schemas.schemas_node_auth import NodeCredentials


async def verify_node(
        node_credentials: NodeCredentials,
        session: AsyncSession
) -> GenericResponseModel[bool]:
    node = await crud_nodes.get_node_by_id(
        node_id=node_credentials.node_id,
        session=session
    )

    if not node:
        raise NodeAuthError('Invalid node credentials')

    if verify_node_access_token(token=node_credentials.token):
        if node.token == node_credentials.token:
            return GenericResponseModel(data=True)

    raise NodeAuthError('Invalid node credentials')
