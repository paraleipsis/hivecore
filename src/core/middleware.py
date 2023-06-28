import uuid

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

DECODE_FORMAT = "latin-1"


async def case_sens_middleware(
        request: Request,
        call_next: RequestResponseEndpoint
) -> Response:
    """Make case-insensitive URLs by converting path and query params to lower case."""
    raw_query_str = request.scope["query_string"].decode(DECODE_FORMAT).lower()
    request.scope["query_string"] = raw_query_str.encode(DECODE_FORMAT)

    path = request.scope["path"].lower()
    request.scope["path"] = path

    response = await call_next(request)

    return response


# async def handle_ssh_conn_middleware(
#         request: Request,
#         call_next: RequestResponseEndpoint
# ) -> Response:
#     path = request.scope["path"].lower()[1:]
#     path_params = path.split('/')
#     if len(path_params) > 1:
#         platform = path_params[1]
#         r = await hello()
#         import json
#         r = json.dumps(r)
#         return Response(content=r, media_type='application/json')
#         # if platform in ('docker', 'swarm'):
#         #     active_conns = get_active_connections()
#         #     node_uuid = path_params[2]
#         #     if node_uuid not in active_conns:
#         #         topic = 'requests'
#         #         request_id = uuid.uuid4()
#         #         value = {
#         #             'url':
#         #         }
#         #         await produce(
#         #             topic=topic,
#         #             key=str(request_id),
#         #             value=new_snapshot
#         #         )
#
#     response = await call_next(request)
#
#     return response


utils = [
    Middleware(BaseHTTPMiddleware, dispatch=case_sens_middleware),
]
