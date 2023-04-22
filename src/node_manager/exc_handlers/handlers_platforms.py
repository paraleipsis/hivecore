from starlette.requests import Request
from starlette.responses import JSONResponse

from node_manager.exc_handlers.exceptions import NoSuchPlatform
from logger.logs import logger
from schemas.response_schemas import GenericResponseModel


async def platform_not_exists_exception_handler(request: Request, exc: NoSuchPlatform):
    logger['debug'].debug(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=404,
        content=GenericResponseModel(success=False, error_msg=str(exc)).dict()
    )
