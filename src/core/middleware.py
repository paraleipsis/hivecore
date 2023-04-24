from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

DECODE_FORMAT = "latin-1"


async def case_sens_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    raw_query_str = request.scope["query_string"].decode(DECODE_FORMAT).lower()
    request.scope["query_string"] = raw_query_str.encode(DECODE_FORMAT)

    path = request.scope["path"].lower()
    request.scope["path"] = path

    response = await call_next(request)
    return response


utils = [
    Middleware(BaseHTTPMiddleware, dispatch=case_sens_middleware),
]
