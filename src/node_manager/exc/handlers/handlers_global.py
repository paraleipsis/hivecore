from starlette.requests import Request
from starlette.responses import JSONResponse

from logger.logs import logger
from node_manager.exc.exceptions import AlreadyExistException
from schemas.response_schemas import GenericResponseModel


async def global_exception_handler(
        request: Request,
        exc: Exception
) -> JSONResponse:
    logger['error'].error(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=500,
        content=GenericResponseModel(success=False).dict()
    )


async def connection_refused_exception_handler(
        request: Request,
        exc: ConnectionRefusedError
) -> JSONResponse:
    logger['error'].error(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=500,
        content=GenericResponseModel(success=False).dict()
    )


async def already_exist_exception_handler(
        request: Request,
        exc: AlreadyExistException
) -> JSONResponse:
    logger['debug'].debug(
        f'{type(exc).__name__}: {str(exc)}'
    )
    return JSONResponse(
        status_code=409,
        content=GenericResponseModel(success=False, error_msg=str(exc)).dict()
    )
