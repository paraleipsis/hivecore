from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from platform_manager import schemas, models
from platform_manager import services
from typing import List

from platform_manager.exceptions import NotFoundException

router = APIRouter(prefix="/platforms", tags=["Platforms"])


@router.get('/', response_model=schemas.GenericResponseModel[List[schemas.PlatformsListRead]])
async def get_all_platforms(session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.get_platforms(session=session)
        return schemas.GenericResponseModel(data=data, total=len(data))
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


@router.post('/', response_model=schemas.GenericResponseModel[schemas.PlatformCreate])
async def create_platform(new_platform: schemas.PlatformCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        await services.add_new_platform(new_platform=new_platform, session=session)

        return schemas.GenericResponseModel(data=new_platform)
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


@router.delete('/{platform_name}', response_model=schemas.GenericResponseModel[bool])
async def delete_platform(platform_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.delete_platform_by_name(platform_name=platform_name, session=session)
        if data:
            return schemas.GenericResponseModel(data=data)
        else:
            raise NotFoundException
    except NotFoundException:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": "Platform not found",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


@router.get('/{platform_name}-environments', response_model=schemas.GenericResponseModel[schemas.PlatformDetailsRead])
async def get_all_platform_environments(platform_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.get_platform_by_name(platform_name=platform_name, session=session)
        return schemas.GenericResponseModel(data=data, total=len(data.environments))
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })




# @router.post('/{platform_name}-environments', response_model=List[EnvironmentRead])
# async def create_platform_environment():
#     pass
#
#
# @router.get('/{platform_name}-environments/{env}')
# async def get_platform_environment():
#     pass
#
#
# @router.delete('/{platform_name}-environments/{env}')
# async def delete_platform_environment():
#     pass
