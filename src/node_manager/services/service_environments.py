from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.exceptions import AlreadyExistException, NoSuchPlatform, NoSuchEnvironment
from node_manager.schemas import schemas_environments
from node_manager.crud import crud_environments, crud_platforms
from core.schemas import core_schemas


async def get_all_environments(
        platform_name: str,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_platforms.get_platform_by_name(platform_name=platform_name, session=session)
        return core_schemas.GenericResponseModel(data=data, total=len(data.environments))
    except NoSuchPlatform:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Platform {platform_name} does not exist",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


async def create_environment(
        platform_name: str,
        new_environment: schemas_environments.EnvironmentCreate,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        await crud_environments.add_new_environment(
            new_environment=new_environment,
            session=session,
            platform_name=platform_name
        )
        return core_schemas.GenericResponseModel(data=new_environment)
    except NoSuchPlatform:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Platform {platform_name} does not exist",
        })
    except AlreadyExistException:
        raise HTTPException(status_code=409, detail={
            "success": False,
            "error_msg": f"Environment with such name in {platform_name} platform already exist",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


async def delete_environment(
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_environments.delete_environment_by_id(
            platform_name=platform_name,
            environment_id=environment_id,
            session=session
        )
        return core_schemas.GenericResponseModel(data=data)
    except NoSuchPlatform:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Platform {platform_name} does not exist",
        })
    except NoSuchEnvironment:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Environment with id {environment_id} does not exist",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })
