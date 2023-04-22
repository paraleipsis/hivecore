import functools


def environment_exceptions(func):
    @functools.wraps(func)
    async def wrap_func(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=str(e)).dict()
            )
        return result

    return wrap_func
