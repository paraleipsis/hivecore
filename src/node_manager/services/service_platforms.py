from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.exceptions import AlreadyExistException, NoSuchPlatform
from node_manager.schemas import schemas_platforms
from node_manager.crud import crud_platforms
from core.schemas import core_schemas


async def get_all_platforms(
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_platforms.get_platforms(session=session)
        return core_schemas.GenericResponseModel(data=data, total=len(data))
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


async def create_platform(
        new_platform: schemas_platforms.PlatformCreate,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        await crud_platforms.add_new_platform(new_platform=new_platform, session=session)
        return core_schemas.GenericResponseModel(data=new_platform)
    except AlreadyExistException:
        raise HTTPException(status_code=409, detail={
            "success": False,
            "error_msg": "Platform with such name already exist",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


async def delete_platform(
        platform_name: str,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_platforms.delete_platform_by_name(platform_name=platform_name, session=session)
        return core_schemas.GenericResponseModel(data=data)
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
