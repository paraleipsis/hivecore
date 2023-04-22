from sqlalchemy.ext.asyncio import AsyncSession

from node_manager.schemas import schemas_environments
from node_manager.crud import crud_environments, crud_platforms
from schemas.response_schemas import GenericResponseModel


async def get_all_environments(
        platform_name: str,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_platforms.get_platform_by_name(platform_name=platform_name, session=session)
    return GenericResponseModel(data=data, total=len(data.environments))


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
        environment_id: int,
        session: AsyncSession
) -> GenericResponseModel:
    data = await crud_environments.delete_environment_by_id(
        platform_name=platform_name,
        environment_id=environment_id,
        session=session
    )
    return GenericResponseModel(data=data)
