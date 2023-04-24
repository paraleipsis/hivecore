from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_environments
from node_manager.crud import crud_environments
from node_manager.utils import is_uuid
from schemas.response_schemas import GenericResponseModel


async def get_all_environments(
        platform_name: str,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_environments.get_platform_environments(
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data, total=len(data))


async def get_environment(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_environments.get_environment(
        environment=environment,
        platform_name=platform_name,
        session=session
    )
    return GenericResponseModel(data=data, total=1)


async def create_environment(
        platform_name: str,
        new_environment: schemas_environments.EnvironmentCreate,
        session: AsyncSession
) -> GenericResponseModel:
    await crud_environments.add_new_environment(
        new_environment=new_environment,
        session=session,
        platform_name=platform_name
    )
    return GenericResponseModel(data=new_environment)


async def delete_environment(
        platform_name: str,
        environment: str | UUID,
        session: AsyncSession
) -> GenericResponseModel:
    if is_uuid(environment):
        data = await crud_environments.delete_environment_by_id(
            platform_name=platform_name,
            environment_id=environment,
            session=session
        )
        return GenericResponseModel(data=data)

    data = await crud_environments.delete_environment_by_name(
        platform_name=platform_name,
        environment_name=environment,
        session=session
    )
    return GenericResponseModel(data=data)
