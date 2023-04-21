from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.exceptions import AlreadyExistException, NoSuchPlatform, NoSuchEnvironment, NoSuchNode
from node_manager.schemas import schemas_nodes
from node_manager.crud import crud_environments, crud_nodes
from core.schemas import core_schemas


async def get_all_nodes(
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_environments.get_environment_by_id(
            environment_id=environment_id,
            platform_name=platform_name,
            session=session
        )
        return core_schemas.GenericResponseModel(data=data, total=len(data.nodes))
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


async def get_node(
        node_id: int,
        platform_name: str,
        environment_id: int,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_nodes.get_node_by_id(
            node_id=node_id,
            environment_id=environment_id,
            platform_name=platform_name,
            session=session
        )
        return core_schemas.GenericResponseModel(data=data)
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


async def create_node(
        platform_name: str,
        environment_id: int,
        new_node: schemas_nodes.NodeCreate,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        await crud_nodes.add_new_node(
            new_node=new_node,
            environment_id=environment_id,
            session=session,
            platform_name=platform_name
        )
        return core_schemas.GenericResponseModel(data=new_node)
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


async def delete_node(
        platform_name: str,
        environment_id: int,
        node_id: int,
        session: AsyncSession
) -> core_schemas.GenericResponseModel:
    try:
        data = await crud_nodes.delete_node_by_id(
            node_id=node_id,
            platform_name=platform_name,
            environment_id=environment_id,
            session=session
        )
        return core_schemas.GenericResponseModel(data=data)
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
