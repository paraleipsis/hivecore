from starlette.requests import Request
from starlette.responses import JSONResponse

from node_manager.exc.exceptions import NoSuchEnvironment
from logger.logs import logger
from modules.schemas.schemas_response import GenericResponseModel


async def environment_not_exists_exception_handler(
        request: Request,
        exc: NoSuchEnvironment
) -> JSONResponse:
    logger['debug'].debug(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=404,
        content=GenericResponseModel(success=False, error_msg=str(exc)).dict()
    )
