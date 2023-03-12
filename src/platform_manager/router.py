from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from platform_manager import schemas, models
from platform_manager import services
from typing import List

from platform_manager.exceptions import AlreadyExistException, NoSuchPlatform, NoSuchEnvironment, NoSuchNode

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


@router.delete('/{platform_name}', response_model=schemas.GenericResponseModel[bool])
async def delete_platform(platform_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.delete_platform_by_name(platform_name=platform_name, session=session)
        return schemas.GenericResponseModel(data=data)
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


@router.get('/{platform_name}', response_model=schemas.GenericResponseModel[schemas.PlatformDetailsRead])
async def get_all_environments(platform_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.get_platform_by_name(platform_name=platform_name, session=session)
        return schemas.GenericResponseModel(data=data, total=len(data.environments))
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


@router.post('/{platform_name}', response_model=schemas.GenericResponseModel[schemas.EnvironmentCreate])
async def create_environment(platform_name: str, new_environment: schemas.EnvironmentCreate,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        await services.add_new_environment(
            new_environment=new_environment,
            session=session,
            platform_name=platform_name
        )
        return schemas.GenericResponseModel(data=new_environment)
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


@router.delete('/{platform_name}/{environment_id}', response_model=schemas.GenericResponseModel[bool])
async def delete_environment(platform_name: str, environment_id: int,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.delete_environment_by_id(
            platform_name=platform_name,
            environment_id=environment_id,
            session=session
        )
        return schemas.GenericResponseModel(data=data)
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


@router.get('/{platform_name}/{environment_id}',
            response_model=schemas.GenericResponseModel[schemas.EnvironmentDetailsRead])
async def get_all_nodes(platform_name: str, environment_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.get_environment_by_id(
            environment_id=environment_id,
            platform_name=platform_name,
            session=session
        )
        return schemas.GenericResponseModel(data=data, total=len(data.nodes))
    except NoSuchEnvironment:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Environment with id {environment_id} does not exist",
        })
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


@router.get('/{platform_name}/{environment_id}/{node_id}',
            response_model=schemas.GenericResponseModel[schemas.NodeRead])
async def get_node(node_id: int, platform_name: str, environment_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.get_node_by_id(
            node_id=node_id,
            environment_id=environment_id,
            platform_name=platform_name,
            session=session
        )
        return schemas.GenericResponseModel(data=data)
    except NoSuchNode:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Node with id {node_id} does not exist",
        })
    except NoSuchEnvironment:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Environment with id {environment_id} does not exist",
        })
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


@router.post('/{platform_name}/{environment_id}', response_model=schemas.GenericResponseModel[schemas.NodeCreate])
async def create_node(platform_name: str, environment_id: int, new_node: schemas.NodeCreate,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        await services.add_new_node(
            new_node=new_node,
            environment_id=environment_id,
            session=session,
            platform_name=platform_name
        )
        return schemas.GenericResponseModel(data=new_node)
    except NoSuchEnvironment:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Environment with id {environment_id} does not exist",
        })
    except NoSuchPlatform:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Platform {platform_name} does not exist",
        })
    except AlreadyExistException:
        raise HTTPException(status_code=409, detail={
            "success": False,
            "error_msg": f"Node with such name in environment with id {environment_id} already exist",
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "data": None,
        })


@router.delete('/{platform_name}/{environment_id}/{node_id}', response_model=schemas.GenericResponseModel[bool])
async def delete_node(platform_name: str, environment_id: int, node_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        data = await services.delete_node_by_id(
            node_id=node_id,
            platform_name=platform_name,
            environment_id=environment_id,
            session=session
        )
        return schemas.GenericResponseModel(data=data)
    except NoSuchNode:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Node with id {node_id} does not exist",
        })
    except NoSuchEnvironment:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error_msg": f"Environment with id {environment_id} does not exist",
        })
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


# @router.delete('/{platform_name}/{environment_id}', response_model=schemas.GenericResponseModel[bool])
# async def delete_environment(platform_name: str, environment_id: int,
#                              session: AsyncSession = Depends(get_async_session)):
#     try:
#         data = await services.delete_environment_by_id(
#             platform_name=platform_name,
#             environment_id=environment_id,
#             session=session
#         )
#         return schemas.GenericResponseModel(data=data)
#     except NoSuchPlatform:
#         raise HTTPException(status_code=404, detail={
#             "success": False,
#             "error_msg": f"Platform {platform_name} does not exist",
#         })
#     except NoSuchEnvironment:
#         raise HTTPException(status_code=404, detail={
#             "success": False,
#             "error_msg": f"Environment with id {environment_id} does not exist",
#         })
#     except Exception:
#         raise HTTPException(status_code=500, detail={
#             "success": False,
#             "data": None,
#         })